"""Day6：运行透明关键词检索，并保留 score 与 source。"""

import json

from src.batterymind.rag_baseline import retrieve


query = "高温为什么会影响电池容量衰减？"
results = retrieve(query, top_k=2)
print(json.dumps({"query": query, "results": results}, ensure_ascii=False, indent=2))
