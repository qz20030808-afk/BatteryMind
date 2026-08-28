"""A real LLM router whose output must pass BatteryMind's decision contract."""

from __future__ import annotations

from typing import Any, Callable

from .decisions import parse_router_decision
from .llm_client import call_chat_model


ROUTER_SYSTEM_PROMPT = """你是 BatteryMind 路由器，只能输出一个 JSON object，不要 Markdown。
字段必须完整：
- route: tool、retrieve、direct 三选一
- tool_name: route=tool 时只能是 inspect_battery_csv，否则必须是 null
- arguments: object；检查 CSV 时必须包含 input_csv
- reason: 一句简短中文理由
用户要求检查 CSV 时选择 tool；询问电池知识时选择 retrieve；其他闲聊选择 direct。"""


def route_question(
    question: str,
    *,
    csv_path: str | None = None,
    call_model: Callable[..., dict[str, Any]] = call_chat_model,
) -> dict[str, Any]:
    """Ask the real model for JSON, then reject anything outside our contract."""

    model_input = question
    if csv_path:
        model_input += f"\n可用 CSV 路径：{csv_path}"
    model_trace = call_model(
        model_input,
        system_prompt=ROUTER_SYSTEM_PROMPT,
        response_format={"type": "json_object"},
        max_tokens=160,
    )
    content = model_trace["response"]["content"] or ""
    decision = parse_router_decision(content)
    return {"decision": decision, "model_trace": model_trace}
