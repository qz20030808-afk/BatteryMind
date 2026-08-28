"""BatteryMind 的统一可运行主链。

这不是新的独立练习，而是把仓库里已经存在的真实部件串起来：

    用户问题
        -> LLM Router（结构化输出）
        -> CSV Tool / RAG / Direct 三选一
        -> 真实观察结果
        -> LLM 根据结果生成最终回答
        -> 稳定 JSON 输出与完整 Trace

所有外部部件都可以在测试中替换成 fake，因此单元测试不会消耗 API 额度；
正常运行时默认使用真实百炼兼容接口。
"""

from __future__ import annotations

import json
from typing import Any, Callable

from .llm_client import call_chat_model
from .llm_router import route_question
from .rag_baseline import retrieve
from .tooling import dispatch_tool


RouteQuestion = Callable[..., dict[str, Any]]
DispatchTool = Callable[[dict[str, Any]], dict[str, Any]]
RetrieveDocuments = Callable[..., list[dict[str, Any]]]
CallModel = Callable[..., dict[str, Any]]


GROUNDED_ANSWER_PROMPT = (
    "你是 BatteryMind 电池助手。只能依据程序提供的工具结果或检索证据回答；"
    "先给结论，再说明关键证据。证据不足或工具失败时不得编造。"
)
DIRECT_ANSWER_PROMPT = (
    "你是 BatteryMind 助手。简洁回答不需要外部工具的普通问题；"
    "如果问题需要电池数据或专业证据，请明确提示用户补充资料。"
)


def _usage_from(model_trace: dict[str, Any] | None) -> dict[str, int]:
    """从一次模型 Trace 中安全取出 Token 统计。"""

    if not model_trace:
        return {}
    usage = model_trace.get("response", {}).get("usage") or {}
    return {
        key: value
        for key, value in usage.items()
        if key in {"prompt_tokens", "completion_tokens", "total_tokens"}
        and isinstance(value, int)
    }


def _usage_summary(
    router_trace: dict[str, Any] | None,
    answer_trace: dict[str, Any] | None,
) -> dict[str, Any]:
    """把 Router 与最终回答两次调用的用量放在同一处。"""

    router = _usage_from(router_trace)
    answer = _usage_from(answer_trace)
    return {
        "router": router,
        "answer": answer,
        "total_tokens": router.get("total_tokens", 0)
        + answer.get("total_tokens", 0),
    }


def _failed_result(
    *,
    request: dict[str, Any],
    trace: list[dict[str, Any]],
    stop_reason: str,
    error: Exception,
    decision: dict[str, Any] | None = None,
    observation: dict[str, Any] | None = None,
    router_trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """把可预期的边界失败也转换成统一输出，而不是只留下堆栈。"""

    error_value = {"type": type(error).__name__, "message": str(error)}
    trace.append(
        {
            "step": len(trace) + 1,
            "event": "pipeline_failed",
            "value": error_value,
        }
    )
    return {
        "request": request,
        "status": "failed",
        "stop_reason": stop_reason,
        "decision": decision,
        "observation": observation,
        "answer": "BatteryMind 本次没有形成可靠回答。",
        "trace": trace,
        "model_traces": {"router": router_trace, "answer": None},
        "usage": _usage_summary(router_trace, None),
        "error": error_value,
    }


def run_batterymind(
    question: str,
    *,
    csv_path: str | None = None,
    route: RouteQuestion = route_question,
    dispatch: DispatchTool = dispatch_tool,
    retrieve_documents: RetrieveDocuments = retrieve,
    answer_with_model: CallModel = call_chat_model,
) -> dict[str, Any]:
    """运行一条完整的 BatteryMind 请求并返回稳定 JSON-ready 结果。

    参数注入只用于测试和后续升级：真实运行不需要传入 route、dispatch、
    retrieve_documents 或 answer_with_model。
    """

    if not question.strip():
        raise ValueError("question 不能为空")

    request = {"question": question, "csv_path": csv_path}
    trace: list[dict[str, Any]] = [
        {"step": 1, "event": "input_received", "value": request}
    ]

    try:
        routed = route(question, csv_path=csv_path)
        decision = routed["decision"]
        router_trace = routed.get("model_trace")
    except Exception as error:
        return _failed_result(
            request=request,
            trace=trace,
            stop_reason="router_failed",
            error=error,
        )

    trace.append(
        {"step": 2, "event": "route_selected", "value": decision}
    )
    route_name = decision["route"]

    if route_name == "tool":
        if not csv_path:
            observation = {
                "kind": "tool",
                "ok": False,
                "tool_name": decision["tool_name"],
                "error": {
                    "type": "MissingUserInput",
                    "message": "Router 选择了 CSV 工具，但用户没有通过 --csv 提供文件路径",
                },
            }
        else:
            # 文件路径来自用户明确输入，而不是信任模型可能编造的参数。
            tool_call = {
                "tool_name": decision["tool_name"],
                "arguments": {**decision["arguments"], "input_csv": csv_path},
            }
            try:
                observation = {"kind": "tool", **dispatch(tool_call)}
            except Exception as error:
                return _failed_result(
                    request=request,
                    trace=trace,
                    stop_reason="tool_execution_failed",
                    error=error,
                    decision=decision,
                    router_trace=router_trace,
                )
        trace.append(
            {"step": 3, "event": "tool_executed", "value": observation}
        )
        if not observation["ok"]:
            trace.append(
                {
                    "step": 4,
                    "event": "guard_stopped",
                    "value": "工具失败，禁止模型假装检查成功",
                }
            )
            return {
                "request": request,
                "status": "needs_attention",
                "stop_reason": "tool_failed",
                "decision": decision,
                "observation": observation,
                "answer": f"CSV 工具执行失败：{observation['error']['message']}",
                "trace": trace,
                "model_traces": {"router": router_trace, "answer": None},
                "usage": _usage_summary(router_trace, None),
            }
        context = json.dumps(observation, ensure_ascii=False)
        answer_prompt = GROUNDED_ANSWER_PROMPT

    elif route_name == "retrieve":
        try:
            documents = retrieve_documents(question, top_k=2)
        except Exception as error:
            return _failed_result(
                request=request,
                trace=trace,
                stop_reason="retrieval_failed",
                error=error,
                decision=decision,
                router_trace=router_trace,
            )
        observation = {
            "kind": "retrieval",
            "ok": bool(documents),
            "documents": documents,
        }
        trace.append(
            {"step": 3, "event": "evidence_retrieved", "value": observation}
        )
        if not documents:
            trace.append(
                {
                    "step": 4,
                    "event": "guard_stopped",
                    "value": "没有检索证据，禁止无依据回答",
                }
            )
            return {
                "request": request,
                "status": "needs_attention",
                "stop_reason": "no_evidence",
                "decision": decision,
                "observation": observation,
                "answer": "当前电池知识库没有找到足够证据，我不能可靠回答。",
                "trace": trace,
                "model_traces": {"router": router_trace, "answer": None},
                "usage": _usage_summary(router_trace, None),
            }
        context = json.dumps(documents, ensure_ascii=False)
        answer_prompt = GROUNDED_ANSWER_PROMPT

    else:
        observation = {
            "kind": "direct",
            "ok": True,
            "message": "Router 判断本题不需要调用外部工具或知识库",
        }
        trace.append(
            {"step": 3, "event": "direct_route_entered", "value": observation}
        )
        context = ""
        answer_prompt = DIRECT_ANSWER_PROMPT

    try:
        answer_trace = answer_with_model(
            question,
            context=context,
            system_prompt=answer_prompt,
            max_tokens=300,
        )
        answer = answer_trace["response"]["content"] or ""
        if not answer.strip():
            raise ValueError("模型返回了空回答")
    except Exception as error:
        return _failed_result(
            request=request,
            trace=trace,
            stop_reason="answer_model_failed",
            error=error,
            decision=decision,
            observation=observation,
            router_trace=router_trace,
        )

    trace.append(
        {
            "step": 4,
            "event": "answer_generated",
            "value": {
                "content": answer,
                "response_id": answer_trace["response"].get("id"),
                "usage": answer_trace["response"].get("usage"),
            },
        }
    )
    trace.append(
        {"step": 5, "event": "pipeline_stopped", "value": "task_complete"}
    )
    return {
        "request": request,
        "status": "completed",
        "stop_reason": "task_complete",
        "decision": decision,
        "observation": observation,
        "answer": answer,
        "trace": trace,
        "model_traces": {"router": router_trace, "answer": answer_trace},
        "usage": _usage_summary(router_trace, answer_trace),
    }
