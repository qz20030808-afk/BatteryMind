"""BatteryMind 统一命令行入口。

示例：
    python -m scripts.run_batterymind "高温为什么影响电池容量？"
    python -m scripts.run_batterymind "检查这份 CSV" --csv tests/fixtures/week2/clean.csv
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
import json
from pathlib import Path
import sys

try:
    from batterymind.app import run_batterymind
except ModuleNotFoundError as error:
    if error.name != "batterymind":
        raise
    raise SystemExit(
        "无法导入 batterymind 项目包。\n"
        f"当前 Python：{sys.executable}\n"
        "请先执行：conda activate batterymind\n"
        "再确认：python -c \"import batterymind; print(batterymind.__file__)\"\n"
        "若仍失败，请在项目根目录执行：python -m pip install -e ."
    ) from error


EXIT_CODES = {"completed": 0, "failed": 1, "needs_attention": 2}


def parse_args() -> Namespace:
    parser = ArgumentParser(description="运行完整 BatteryMind Agent 主链")
    parser.add_argument("question", help="准备交给 BatteryMind 的问题")
    parser.add_argument(
        "--csv",
        dest="csv_path",
        help="可选：需要检查的电池循环 CSV 路径",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="可选：把完整 JSON 结果同时保存到文件",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="不缩进 JSON，适合交给其他程序读取",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_batterymind(args.question, csv_path=args.csv_path)
    text = json.dumps(
        result,
        ensure_ascii=False,
        indent=None if args.compact else 2,
    )
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    return EXIT_CODES[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
