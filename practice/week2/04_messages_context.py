"""Day3：观察 messages 进入有限上下文时的取舍。"""

import json


messages = [
    {"role": "system", "content": "只能根据证据回答。", "budget_units": 5},
    {"role": "assistant", "content": "上一次对话的长摘要", "budget_units": 9},
    {"role": "user", "content": "证据：高温可能加速老化。问题：温度为何重要？", "budget_units": 12},
]
budget = 20

# 这里只用人工标注的 budget_units 展示取舍，不冒充真实 tokenizer 计数。
kept = [messages[0], messages[-1]]
used = sum(message["budget_units"] for message in kept)

print(json.dumps({"budget": budget, "used": used, "kept": kept}, ensure_ascii=False, indent=2))
