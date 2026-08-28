"""Day4：让真实模型生成 RouterDecision，再由 Python 校验。"""

import json

from src.batterymind.llm_client import ModelConfigurationError
from src.batterymind.llm_router import route_question


try:
    result = route_question(
        "请检查这个电池 CSV 的数据质量",
        csv_path="tests/fixtures/week2/clean.csv",
    )
except ModelConfigurationError as error:
    print(f"配置未完成：{error}")
    raise SystemExit(2) from error

print(json.dumps(result, ensure_ascii=False, indent=2))
