"""Day5：执行一次真实模型 Tool Calling 往返。"""

import json

from src.batterymind.llm_client import ModelConfigurationError
from src.batterymind.real_tool_agent import run_real_tool_agent


try:
    result = run_real_tool_agent(
        "请使用工具检查 tests/fixtures/week2/clean.csv 的数据质量，并总结结果。"
    )
except ModelConfigurationError as error:
    print(f"配置未完成：{error}")
    raise SystemExit(2) from error

print(json.dumps(result, ensure_ascii=False, indent=2))
