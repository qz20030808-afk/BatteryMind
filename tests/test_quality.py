"""Week 2 数据质量报告测试。

正确运行：python -m pytest tests/test_quality.py -q
不要使用 VS Code 的“运行 Python 文件”直接执行测试集合。
"""

import json
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pytest

from scripts.quality import (
    build_report,
    count_duplicates,
    count_missing,
    count_out_of_range,
    find_cycle_issues,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "week2"
SCRIPT_MODULE = "scripts.quality"


def read_fixture(name: str) -> pd.DataFrame:
    """测试辅助函数：统一读取 Week 2 fixture。"""
    return pd.read_csv(FIXTURES / name)


def run_cli(name: str) -> subprocess.CompletedProcess[str]:
    """使用当前测试解释器运行真实 CLI，并捕获 JSON 与退出码。"""
    return subprocess.run(
        [sys.executable, "-m", SCRIPT_MODULE, str(FIXTURES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_clean_data_has_no_quality_issues() -> None:
    report = build_report(read_fixture("clean.csv"))

    assert report["quality_ok"] is True
    assert report["missing"] == {}
    assert report["duplicate_rows"] == 0
    assert report["out_of_range"] == {}
    assert report["cycle_issues"] == []


def test_issue_data_reports_all_four_quality_dimensions() -> None:
    report = build_report(read_fixture("issues.csv"))

    assert report["quality_ok"] is False
    assert report["missing"] == {"capacity": 1}
    assert report["duplicate_rows"] == 1
    assert report["out_of_range"] == {"capacity": 1, "voltage": 1, "temperature": 1}
    assert report["cycle_issues"] == ["B001", "B002"]


@pytest.mark.parametrize(
    ("check", "expected"),
    [
        (count_missing, {"capacity": 1}),
        (count_duplicates, 1),
        (count_out_of_range, {"capacity": 1, "voltage": 1, "temperature": 1}),
        (find_cycle_issues, ["B001", "B002"]),
    ],
)
def test_each_quality_check_can_run_independently(check, expected) -> None:
    assert check(read_fixture("issues.csv")) == expected


@pytest.mark.parametrize(
    ("fixture_name", "expected_code", "expected_status"),
    [
        ("clean.csv", 0, "pass"),
        ("issues.csv", 2, "quality_issues"),
    ],
)
def test_cli_status_matches_data_quality(
    fixture_name: str,
    expected_code: int,
    expected_status: str,
) -> None:
    completed = run_cli(fixture_name)
    payload = json.loads(completed.stdout)

    assert completed.returncode == expected_code
    assert payload["status"] == expected_status


def test_cli_can_write_the_same_json_to_a_file(tmp_path: Path) -> None:
    output = tmp_path / "quality.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            SCRIPT_MODULE,
            str(FIXTURES / "clean.csv"),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert completed.returncode == 0
    assert json.loads(output.read_text(encoding="utf-8")) == json.loads(completed.stdout)
