"""BatteryMind Week 2：电池 CSV 数据质量报告。

本周只维护这一份主文件，避免为每个 Pandas 知识点创建重复脚本。
它同时承担两种角色：

1. 其他 Python 代码可以 import 这里的小函数；
2. 人、CI 或后续 Agent 可以通过 CLI 运行完整检查。

从 BatteryMind 根目录运行：

    python -m scripts.quality tests/fixtures/week2/clean.csv --pretty
    python -m scripts.quality tests/fixtures/week2/issues.csv --pretty
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
import json
from pathlib import Path
import sys

import pandas as pd

from scripts.inspect_csv import find_missing_columns, load_csv, validate_input_path


# 这些是 Week 2 的教学规则，不是所有电池数据都通用的物理真理。
# 后续拿到真实企业数据时，应根据电池体系、量纲和业务要求配置。
RANGES: dict[str, tuple[float, float]] = {
    "capacity": (0.0, 10.0),
    "voltage": (0.0, 5.0),
    "temperature": (-40.0, 100.0),
}


def count_missing(dataframe: pd.DataFrame) -> dict[str, int]:
    """返回真正存在缺失值的列及其数量。"""
    missing_mask = dataframe.isna()
    missing_counts = missing_mask.sum()
    return {
        str(column): int(count)
        for column, count in missing_counts.items()
        if count > 0
    }


def count_duplicates(dataframe: pd.DataFrame) -> int:
    """返回重复行数量；第一次出现不算重复，后续重复才计数。"""
    duplicate_mask = dataframe.duplicated()
    duplicate_count = duplicate_mask.sum()
    return int(duplicate_count)


def count_out_of_range(
    dataframe: pd.DataFrame,
    ranges: dict[str, tuple[float, float]] = RANGES,
) -> dict[str, int]:
    """按列统计小于下限或大于上限的值。缺失值由 count_missing 负责。"""
    violations: dict[str, int] = {}

    for column, (minimum, maximum) in ranges.items():
        if column not in dataframe.columns:
            continue

        numeric = pd.to_numeric(dataframe[column], errors="coerce")
        count = int(((numeric < minimum) | (numeric > maximum)).sum())
        if count > 0:
            violations[column] = count

    return violations


def find_cycle_issues(dataframe: pd.DataFrame) -> list[str]:
    """找出 cycle 没有严格递增的 battery_id。"""
    required = {"battery_id", "cycle"}
    if not required.issubset(dataframe.columns):
        return []

    issue_ids: list[str] = []
    for battery_id, group in dataframe.groupby("battery_id", sort=False):
        cycles = pd.to_numeric(group["cycle"], errors="coerce").tolist()
        has_issue = any(
            pd.isna(current) or pd.isna(previous) or current <= previous
            for previous, current in zip(cycles, cycles[1:])
        )
        if has_issue:
            issue_ids.append(str(battery_id))

    return issue_ids


def build_report(dataframe: pd.DataFrame) -> dict[str, object]:
    """把四类检查接成稳定、可序列化的数据质量报告。"""
    missing = count_missing(dataframe)
    duplicates = count_duplicates(dataframe)
    out_of_range = count_out_of_range(dataframe)
    cycle_issues = find_cycle_issues(dataframe)

    quality_ok = not any([missing, duplicates, out_of_range, cycle_issues])
    return {
        "quality_ok": quality_ok,
        "row_count": int(dataframe.shape[0]),
        "column_count": int(dataframe.shape[1]),
        "missing": missing,
        "duplicate_rows": duplicates,
        "out_of_range": out_of_range,
        "cycle_issues": cycle_issues,
    }


def parse_args() -> Namespace:
    """声明 CLI 接受的位置参数和带名字选项。"""
    parser = ArgumentParser(description="生成 BatteryMind CSV 数据质量报告")
    parser.add_argument("input_csv", type=Path, help="准备检查的 CSV 路径")
    parser.add_argument("--output", type=Path, help="可选：把 JSON 同时写入这个文件")
    parser.add_argument("--pretty", action="store_true", help="使用缩进输出，方便人阅读")
    return parser.parse_args()


def emit_json(payload: dict[str, object], output: Path | None, pretty: bool) -> None:
    """统一控制终端输出和可选文件输出。"""
    indent = 2 if pretty else None
    json_text = json.dumps(payload, ensure_ascii=False, indent=indent)
    print(json_text)

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json_text + "\n", encoding="utf-8")


def main() -> int:
    """运行完整链路，并用退出码区分通过、数据问题和程序错误。"""
    args = parse_args()

    try:
        validate_input_path(args.input_csv)
        dataframe = load_csv(args.input_csv)
        missing_columns = find_missing_columns(dataframe)
        if missing_columns:
            raise ValueError(f"缺少核心字段：{missing_columns}")
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        emit_json(
            {
                "status": "error",
                "file": str(args.input_csv),
                "error_type": type(error).__name__,
                "message": str(error),
            },
            args.output,
            args.pretty,
        )
        return 1

    report = build_report(dataframe)
    status = "pass" if report["quality_ok"] else "quality_issues"
    emit_json(
        {"status": status, "file": str(args.input_csv), "report": report},
        args.output,
        args.pretty,
    )
    return 0 if report["quality_ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
