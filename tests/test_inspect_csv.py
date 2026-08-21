"""第 1 周自动化验收：文件已准备好，Day 5 用来学习 pytest 结构。

学习方式：先运行全部测试，再逐个对应 Arrange / Act / Assert。
不需要重新抄写这些测试。
"""

from pathlib import Path
import sys


if __name__ == "__main__":
    print("这个文件是 pytest 测试文件，不是普通 Python 脚本入口。")
    print(f"你刚才使用的 Python：{sys.executable}")
    print("请在 BatteryMind 根目录运行：")
    print(r"  D:\Anaconda\envs\batterymind\python.exe -m pytest tests\test_inspect_csv.py -q")
    print("或者先 conda activate batterymind，再运行 python -m pytest tests\\test_inspect_csv.py -q")
    raise SystemExit(2)

import pytest

from scripts.inspect_csv import find_missing_columns, load_csv, validate_input_path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "week1"


def test_valid_csv_can_be_loaded_and_has_no_missing_core_columns() -> None:
    # Arrange：准备一个有效输入。
    csv_path = FIXTURE_DIR / "valid.csv"

    # Act：执行真实项目函数。
    validate_input_path(csv_path)
    dataframe = load_csv(csv_path)
    missing_columns = find_missing_columns(dataframe)

    # Assert：固定我们承诺的结果。
    assert dataframe.shape == (3, 5)
    assert missing_columns == []


def test_missing_capacity_is_reported_before_column_is_used() -> None:
    csv_path = FIXTURE_DIR / "missing_capacity.csv"
    dataframe = load_csv(csv_path)

    assert find_missing_columns(dataframe) == ["capacity"]


def test_missing_file_is_rejected() -> None:
    csv_path = FIXTURE_DIR / "not_exists.csv"

    with pytest.raises(FileNotFoundError, match="文件不存在"):
        validate_input_path(csv_path)


def test_wrong_extension_is_rejected() -> None:
    csv_path = FIXTURE_DIR / "wrong_extension.txt"

    with pytest.raises(ValueError, match="后缀必须是 .csv"):
        validate_input_path(csv_path)


def test_empty_file_is_rejected() -> None:
    csv_path = FIXTURE_DIR / "empty.csv"

    with pytest.raises(ValueError, match="文件为空"):
        validate_input_path(csv_path)


def test_directory_is_not_treated_as_csv_file() -> None:
    with pytest.raises(ValueError, match="路径不是文件"):
        validate_input_path(FIXTURE_DIR)
