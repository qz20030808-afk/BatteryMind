import json

import pytest

from batterymind.decisions import DecisionValidationError, parse_router_decision


def test_valid_tool_decision_is_accepted() -> None:
    value = {"route": "tool", "tool_name": "inspect_battery_csv", "arguments": {"input_csv": "a.csv"}, "reason": "检查"}
    assert parse_router_decision(json.dumps(value, ensure_ascii=False)) == value


@pytest.mark.parametrize("value", [
    {"route": "tool", "tool_name": "delete_files", "arguments": {}, "reason": "危险"},
    {"route": "retrieve", "tool_name": None, "reason": "缺字段"},
])
def test_invalid_decisions_are_rejected(value: dict[str, object]) -> None:
    with pytest.raises(DecisionValidationError):
        parse_router_decision(json.dumps(value, ensure_ascii=False))
