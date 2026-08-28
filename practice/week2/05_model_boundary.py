"""Day4：不隐藏 SDK 细节，完成第一次真实模型 API 调用。"""

import json
import os

from openai import OpenAI


api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    print("配置未完成：当前 PowerShell 没有 DASHSCOPE_API_KEY")
    print("请按网站 16.1 的教程安全输入 Key，再重新运行。")
    raise SystemExit(2)

base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model = "qwen3.7-plus"
messages = [
    {
        "role": "system",
        "content": "你是 BatteryMind 助手，只能根据给定证据回答。",
    },
    {
        "role": "user",
        "content": "证据：循环会消耗活性锂，高温可能加速副反应。\n问题：电池容量为什么会衰减？",
    },
]

client = OpenAI(api_key=api_key, base_url=base_url, timeout=60.0)

try:
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=96,
    )
except Exception as error:
    print(f"真实 API 调用失败：{type(error).__name__}: {error}")
    raise SystemExit(1) from error

choice = completion.choices[0]
result = {
    "request": {"base_url": base_url, "model": model, "messages": messages},
    "response": {
        "id": completion.id,
        "model": completion.model,
        "content": choice.message.content,
        "finish_reason": choice.finish_reason,
        "usage": completion.usage.model_dump() if completion.usage else None,
    },
}

print(json.dumps(result, ensure_ascii=False, indent=2))
