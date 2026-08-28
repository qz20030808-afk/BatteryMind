"""One authentic model -> tool -> observation -> model round trip."""

from __future__ import annotations

import json
from typing import Any, Callable

from .llm_client import call_chat_completion, load_model_settings
from .tooling import TOOL_SCHEMAS, dispatch_tool


SYSTEM_PROMPT = (
    "你是 BatteryMind Agent。用户要求检查 CSV 时必须调用 inspect_battery_csv；"
    "收到工具结果后，只根据结果用中文总结，不要编造字段。"
)


def run_real_tool_agent(
    question: str,
    *,
    call_completion: Callable[..., dict[str, Any]] = call_chat_completion,
    settings: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Let the model choose the tool, execute it locally, then ask for a final answer."""

    resolved_settings = settings or load_model_settings()
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    first = call_completion(
        messages,
        tools=TOOL_SCHEMAS,
        tool_choice="auto",
        max_tokens=160,
        settings=resolved_settings,
    )
    proposed_calls = first["response"]["tool_calls"]
    if not proposed_calls:
        return {
            "answer": first["response"]["content"],
            "trace": [{"event": "model_response", "value": first["response"]}],
            "stop_reason": "model_answered_without_tool",
        }

    call = proposed_calls[0]
    arguments = json.loads(call["arguments"])
    tool_call = {"tool_name": call["name"], "arguments": arguments}
    observation = dispatch_tool(tool_call)

    messages.append(
        {
            "role": "assistant",
            "content": first["response"]["content"],
            "tool_calls": [
                {
                    "id": call["id"],
                    "type": "function",
                    "function": {"name": call["name"], "arguments": call["arguments"]},
                }
            ],
        }
    )
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call["id"],
            "content": json.dumps(observation, ensure_ascii=False),
        }
    )
    final = call_completion(
        messages,
        tools=TOOL_SCHEMAS,
        max_tokens=200,
        settings=resolved_settings,
    )
    return {
        "answer": final["response"]["content"],
        "observation": observation,
        "trace": [
            {"event": "tool_call", "value": call},
            {"event": "observation", "value": observation},
            {"event": "final_model_response", "value": final["response"]},
        ],
        "stop_reason": "task_complete",
    }
