"""Safe Tool Calling boundary for BatteryMind's deterministic CSV checker."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pandas as pd

from scripts.inspect_csv import find_missing_columns, load_csv, validate_input_path
from scripts.quality import build_report


TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "inspect_battery_csv",
            "description": "读取电池循环 CSV，检查核心字段并生成结构化数据质量报告。",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_csv": {
                        "type": "string",
                        "description": "相对于 BatteryMind 根目录或绝对 CSV 路径",
                    }
                },
                "required": ["input_csv"],
                "additionalProperties": False,
            },
        },
    }
]


def inspect_battery_csv(input_csv: str) -> dict[str, Any]:
    """Reuse tested Week1/2 functions and expose one stable tool result."""

    path = Path(input_csv)
    validate_input_path(path)
    dataframe = load_csv(path)
    missing_columns = find_missing_columns(dataframe)
    if missing_columns:
        raise ValueError(f"缺少核心字段：{missing_columns}")
    return {"file": str(path), "report": build_report(dataframe)}


TOOL_REGISTRY: dict[str, Callable[..., dict[str, Any]]] = {
    "inspect_battery_csv": inspect_battery_csv,
}


def dispatch_tool(tool_call: dict[str, Any]) -> dict[str, Any]:
    """Validate a model-proposed call, execute an allow-listed function, wrap errors."""

    tool_name = tool_call.get("tool_name")
    arguments = tool_call.get("arguments")
    if tool_name not in TOOL_REGISTRY:
        return {
            "ok": False,
            "tool_name": tool_name,
            "error": {"type": "UnknownTool", "message": "工具不在白名单"},
        }
    if not isinstance(arguments, dict):
        return {
            "ok": False,
            "tool_name": tool_name,
            "error": {"type": "InvalidArguments", "message": "arguments 必须是对象"},
        }

    try:
        data = TOOL_REGISTRY[tool_name](**arguments)
    except (FileNotFoundError, TypeError, ValueError, pd.errors.ParserError) as error:
        return {
            "ok": False,
            "tool_name": tool_name,
            "error": {"type": type(error).__name__, "message": str(error)},
        }
    return {"ok": True, "tool_name": tool_name, "data": data}
