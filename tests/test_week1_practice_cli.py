"""保护 09B 教学练习的真实成功/失败行为。"""

import json
import os
from pathlib import Path
import subprocess
import sys


if __name__ == "__main__":
    print("这个文件由 pytest 收集运行，不应该使用“运行 Python 文件”。")
    print(f"你刚才使用的 Python：{sys.executable}")
    print(r"请运行：D:\Anaconda\envs\batterymind\python.exe -m pytest tests\test_week1_practice_cli.py -q")
    raise SystemExit(2)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "practice" / "week1" / "09b_json_and_exit_code.py"
VALID_CSV = PROJECT_ROOT / "tests" / "fixtures" / "week1" / "valid.csv"
MISSING_CSV = PROJECT_ROOT / "tests" / "fixtures" / "week1" / "not_exists.csv"


def run_practice(input_path: Path) -> subprocess.CompletedProcess[str]:
    """使用当前测试环境中的 Python 运行 09B，并捕获输出与退出码。"""
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(input_path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )


def test_json_practice_reports_real_success() -> None:
    completed = run_practice(VALID_CSV)
    result = json.loads(completed.stdout)

    assert completed.returncode == 0
    assert result["ok"] is True
    assert result["file"] == str(VALID_CSV)


def test_json_practice_reports_real_failure() -> None:
    completed = run_practice(MISSING_CSV)
    result = json.loads(completed.stdout)

    assert completed.returncode == 1
    assert result["ok"] is False
    assert result["error_type"] == "FileNotFoundError"
