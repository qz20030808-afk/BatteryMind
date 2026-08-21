"""BatteryMind 第 1 周主脚本：CSV 输入检查器（Day 3 教学版本）。

文件已经提前创建，避免学习过程中重复建文件和复制大段骨架。
Day 3 先理解并运行 Path、Pandas 和集合检查；Day 4 再在同一个文件上
逐步加入 argparse、JSON 和退出码。
"""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"battery_id", "cycle", "capacity"}
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = PROJECT_ROOT / "tests" / "fixtures" / "week1" / "valid.csv"


def validate_input_path(csv_path: Path) -> None:
    """检查文件是否存在、是否为文件、后缀和大小是否正确。"""
    if not csv_path.exists():
        raise FileNotFoundError(f"文件不存在：{csv_path}")
    if not csv_path.is_file():
        raise ValueError(f"路径不是文件：{csv_path}")
    if csv_path.suffix.lower() != ".csv":
        raise ValueError(f"文件后缀必须是 .csv：{csv_path.suffix}")
    if csv_path.stat().st_size == 0:
        raise ValueError(f"文件为空：{csv_path}")


def load_csv(csv_path: Path) -> pd.DataFrame:
    """用 Pandas 读取 CSV，并确保表格至少有一行数据。"""
    dataframe = pd.read_csv(csv_path)
    if dataframe.empty:
        raise ValueError(f"CSV 没有数据行：{csv_path}")
    return dataframe


def find_missing_columns(dataframe: pd.DataFrame) -> list[str]:
    """使用集合差集返回缺少的核心字段。"""
    actual_columns = set(dataframe.columns)
    missing_columns = REQUIRED_COLUMNS - actual_columns
    return sorted(missing_columns)


def run_day3_demo() -> None:
    """把 Day 1～Day 3 学到的能力接成第一条可运行链路。"""
    validate_input_path(DEMO_PATH)
    dataframe = load_csv(DEMO_PATH)
    missing_columns = find_missing_columns(dataframe)

    print(f"读取文件：{DEMO_PATH.name}")
    print(f"DataFrame 形状：{dataframe.shape}")
    print(f"实际字段：{dataframe.columns.tolist()}")
    print(f"缺失核心字段：{missing_columns}")


if __name__ == "__main__":
    run_day3_demo()
