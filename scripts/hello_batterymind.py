import platform
import sys
from pathlib import Path

import pandas as pd


def get_project_root() -> Path:
    """返回 BatteryMind 项目根目录。"""
    return Path(__file__).resolve().parents[1]


def main() -> None:
    project_root = get_project_root()

    print("BatteryMind environment check")
    print(f"Project root: {project_root}")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Python executable: {sys.executable}")
    print(f"Operating system: {platform.platform()}")
    print(f"Pandas version: {pd.__version__}")


if __name__ == "__main__":
    main()