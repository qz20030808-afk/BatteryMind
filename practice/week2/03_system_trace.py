"""Day3：先看 BatteryMind 最终产品由哪些层组成。"""

import json


LAYERS = [
    {"layer": 1, "name": "用户入口", "job": "接收问题和文件", "status": "next"},
    {"layer": 2, "name": "Agent 决策", "job": "选择检索、数据工具或直接回答", "status": "prototype"},
    {"layer": 3, "name": "Tool Dispatcher", "job": "校验并执行白名单工具", "status": "next"},
    {"layer": 4, "name": "CSV 质量工具", "job": "检查字段和数据质量", "status": "done"},
    {"layer": 5, "name": "RAG", "job": "返回带来源的电池知识", "status": "next"},
    {"layer": 6, "name": "SOH 模型", "job": "给出预测与置信信息", "status": "future"},
    {"layer": 7, "name": "Verifier 与回答", "job": "检查证据、组织答案并保存 Trace", "status": "future"},
]

print(json.dumps(LAYERS, ensure_ascii=False, indent=2))
