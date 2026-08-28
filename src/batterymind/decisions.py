"""Parse and validate a model-generated BatteryMind routing decision."""

from __future__ import annotations

import json
from typing import Any


ALLOWED_ROUTES = {"tool", "retrieve", "direct"}
ALLOWED_TOOLS = {"inspect_battery_csv"}


class DecisionValidationError(ValueError):
    """Raised when model output is readable JSON but violates our contract."""


def parse_router_decision(text: str) -> dict[str, Any]:
    """Turn JSON text into a decision only after structural and business checks."""

    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise DecisionValidationError(f"不是合法 JSON：{error.msg}") from error

    if not isinstance(value, dict):
        raise DecisionValidationError("决策最外层必须是 JSON object")

    required = {"route", "tool_name", "arguments", "reason"}
    missing = sorted(required - value.keys())
    if missing:
        raise DecisionValidationError(f"缺少字段：{missing}")

    if value["route"] not in ALLOWED_ROUTES:
        raise DecisionValidationError(f"不允许的 route：{value['route']}")
    if not isinstance(value["arguments"], dict):
        raise DecisionValidationError("arguments 必须是 JSON object")
    if not isinstance(value["reason"], str):
        raise DecisionValidationError("reason 必须是字符串")

    if value["route"] == "tool":
        if value["tool_name"] not in ALLOWED_TOOLS:
            raise DecisionValidationError(f"工具不在白名单：{value['tool_name']}")
        input_csv = value["arguments"].get("input_csv")
        if not isinstance(input_csv, str) or not input_csv.strip():
            raise DecisionValidationError("inspect_battery_csv 需要非空 input_csv")
    elif value["tool_name"] is not None:
        raise DecisionValidationError("非 tool 路由的 tool_name 必须是 null")

    return value
