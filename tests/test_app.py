from typing import Any

from batterymind.app import run_batterymind


def fake_model_answer(
    question: str,
    *,
    context: str = "",
    system_prompt: str,
    max_tokens: int,
) -> dict[str, Any]:
    return {
        "request": {"messages": [{"role": "user", "content": question}]},
        "response": {
            "id": "answer-test",
            "content": f"已依据本轮信息回答：{question}",
            "usage": {
                "prompt_tokens": 30,
                "completion_tokens": 12,
                "total_tokens": 42,
            },
        },
    }


def make_router(decision: dict[str, Any]):
    def fake_router(question: str, *, csv_path: str | None = None):
        return {
            "decision": decision,
            "model_trace": {
                "response": {"content": "{}", "usage": {"total_tokens": 18}}
            },
        }

    return fake_router


def test_tool_route_connects_router_real_csv_tool_and_final_answer() -> None:
    router = make_router(
        {
            "route": "tool",
            "tool_name": "inspect_battery_csv",
            "arguments": {"input_csv": "tests/fixtures/week2/clean.csv"},
            "reason": "用户要求检查 CSV",
        }
    )

    result = run_batterymind(
        "检查这份 CSV",
        csv_path="tests/fixtures/week2/clean.csv",
        route=router,
        answer_with_model=fake_model_answer,
    )

    assert result["status"] == "completed"
    assert result["decision"]["route"] == "tool"
    assert result["observation"]["data"]["report"]["quality_ok"] is True
    assert [item["event"] for item in result["trace"]] == [
        "input_received",
        "route_selected",
        "tool_executed",
        "answer_generated",
        "pipeline_stopped",
    ]
    assert result["usage"]["total_tokens"] == 60


def test_retrieve_route_passes_source_preserving_evidence_to_model() -> None:
    captured: dict[str, str] = {}

    def answer_model(question: str, *, context: str, **kwargs):
        captured["context"] = context
        return fake_model_answer(question, context=context, **kwargs)

    router = make_router(
        {
            "route": "retrieve",
            "tool_name": None,
            "arguments": {},
            "reason": "需要电池知识",
        }
    )
    result = run_batterymind(
        "高温为什么影响电池容量？",
        route=router,
        answer_with_model=answer_model,
    )

    assert result["status"] == "completed"
    assert result["observation"]["kind"] == "retrieval"
    assert "BatteryMind 教学知识库" in captured["context"]
    assert result["trace"][2]["event"] == "evidence_retrieved"


def test_no_evidence_stops_before_answer_model_can_hallucinate() -> None:
    def answer_must_not_run(*args, **kwargs):
        raise AssertionError("没有证据时不应调用最终回答模型")

    router = make_router(
        {
            "route": "retrieve",
            "tool_name": None,
            "arguments": {},
            "reason": "需要外部证据",
        }
    )
    result = run_batterymind(
        "南京今天堵不堵车？",
        route=router,
        answer_with_model=answer_must_not_run,
    )

    assert result["status"] == "needs_attention"
    assert result["stop_reason"] == "no_evidence"
    assert result["model_traces"]["answer"] is None


def test_failed_tool_returns_visible_error_without_fake_success() -> None:
    router = make_router(
        {
            "route": "tool",
            "tool_name": "inspect_battery_csv",
            "arguments": {"input_csv": "missing.csv"},
            "reason": "用户要求检查 CSV",
        }
    )
    result = run_batterymind(
        "检查不存在的文件",
        route=router,
        answer_with_model=fake_model_answer,
    )

    assert result["status"] == "needs_attention"
    assert result["stop_reason"] == "tool_failed"
    assert "失败" in result["answer"]
    assert result["model_traces"]["answer"] is None


def test_tool_route_requires_csv_path_from_user_not_model_hallucination() -> None:
    router = make_router(
        {
            "route": "tool",
            "tool_name": "inspect_battery_csv",
            "arguments": {"input_csv": "model-invented.csv"},
            "reason": "用户要求检查 CSV",
        }
    )

    result = run_batterymind(
        "检查 CSV",
        route=router,
        answer_with_model=fake_model_answer,
    )

    assert result["status"] == "needs_attention"
    assert result["observation"]["error"]["type"] == "MissingUserInput"
    assert result["model_traces"]["answer"] is None


def test_retriever_exception_is_assigned_to_retrieval_layer() -> None:
    router = make_router(
        {
            "route": "retrieve",
            "tool_name": None,
            "arguments": {},
            "reason": "需要电池知识",
        }
    )

    def broken_retriever(question: str, *, top_k: int):
        raise OSError("knowledge index unavailable")

    result = run_batterymind(
        "电池容量衰减是什么？",
        route=router,
        retrieve_documents=broken_retriever,
    )

    assert result["status"] == "failed"
    assert result["stop_reason"] == "retrieval_failed"
    assert result["error"]["type"] == "OSError"


def test_direct_route_still_uses_model_but_no_external_evidence() -> None:
    router = make_router(
        {
            "route": "direct",
            "tool_name": None,
            "arguments": {},
            "reason": "普通问候",
        }
    )
    result = run_batterymind(
        "你好，请介绍一下你自己",
        route=router,
        answer_with_model=fake_model_answer,
    )

    assert result["status"] == "completed"
    assert result["observation"]["kind"] == "direct"
    assert result["trace"][2]["event"] == "direct_route_entered"


def test_router_exception_becomes_stable_failed_result() -> None:
    def broken_router(question: str, *, csv_path: str | None = None):
        raise ConnectionError("router service unavailable")

    result = run_batterymind("高温影响", route=broken_router)

    assert result["status"] == "failed"
    assert result["stop_reason"] == "router_failed"
    assert result["error"]["type"] == "ConnectionError"
