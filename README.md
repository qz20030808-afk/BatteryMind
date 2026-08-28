# BatteryMind Foundation

BatteryMind Foundation 是我学习 AI Agent 工程时完成的第一阶段项目。它的价值是把真实大模型调用、结构化路由、确定性 CSV 工具、轻量关键词检索、失败保护和可测试 Trace 串成一条可运行链路；它不是最终用于求职展示的完整电池智能系统。

本仓库在这一阶段冻结。真实电池数据、向量知识库、Embedding 检索、SOH 模型和多步 Agent 编排将在独立的第二项目中实现，不在这里把未来能力写成已经完成。

## 当前真正实现的能力

- 通过百炼 OpenAI-compatible API 调用真实大模型；
- 用结构化 RouterDecision 把问题分为 `tool`、`retrieve` 或 `direct`；
- 使用 Pandas 检查 CSV 的字段、缺失、重复、范围和循环顺序；
- 通过白名单 Dispatcher 执行 `inspect_battery_csv`；
- 提供一个独立的 API 原生 Function Calling 往返原型；
- 使用小型本地 JSON 词条做透明关键词检索基线；
- 返回统一的 `status`、`stop_reason`、`observation`、`trace` 和 Token 用量；
- 用 pytest 覆盖成功路线和主要失败边界。

## 当前没有实现的能力

- 没有使用真实公开电池时序数据集；测试 CSV 只是用于验证程序边界的小型 fixture；
- 没有生产级知识库、文档切块、Embedding、向量索引或检索评测；
- 统一主入口的工具路线仍是 RouterDecision + Python Dispatcher，不是 API 原生 Function Calling；
- 没有接入 SOH 训练模型、模型权重、在线传感器数据或不确定性估计；
- 没有多步自主规划、循环反思、持久化 Memory 或 LangGraph 主链；
- 没有 Web 服务、鉴权、监控和生产部署。

因此，这个仓库适合证明“我理解并实现过 Agent 应用的基本部件和工程边界”，不适合宣称“完成了企业级 Agentic RAG 或电池健康诊断系统”。

## 当前行动链

```text
question + 可选 csv_path
          ↓
真实 LLM Router
          ↓
经过校验的 RouterDecision
          ├─ tool     → Python Dispatcher → CSV Tool
          ├─ retrieve → 本地关键词检索基线
          └─ direct   → 不调用外部能力
          ↓
失败 / 无证据 Guard
          ↓
真实 LLM 根据 Observation 生成回答
          ↓
status + stop_reason + answer + trace + usage
```

这里必须区分两条工具路线：

1. `src/batterymind/app.py` 是当前统一主链，程序根据 RouterDecision 手动调用 Dispatcher；
2. `src/batterymind/real_tool_agent.py` 是独立的 API 原生 Function Calling 原型，包含“模型返回 `tool_calls` → Python 执行工具 → Tool 结果回传模型”的两次请求。

第二条目前没有接入第一条，因此 README 不把两者描述成同一条已完成链路。

## 运行

从项目根目录开始：

```powershell
conda activate batterymind
Set-Location -LiteralPath 'C:\Users\qiuzhe\Desktop\work\BatteryMind'
python -m pip install -e .
python -c "import sys, batterymind; print(sys.executable); print(batterymind.__file__)"
```

真实模型调用需要当前环境中存在 `DASHSCOPE_API_KEY`。项目默认使用百炼兼容地址和 Qwen Chat 模型。

运行关键词检索路线：

```powershell
python -m scripts.run_batterymind "高温为什么可能加速电池容量衰减？"
```

运行 CSV 工具路线：

```powershell
python -m scripts.run_batterymind "请检查这份 CSV 的数据质量" --csv tests/fixtures/week2/clean.csv
```

运行自动测试：

```powershell
python -m pytest -q
```

测试使用受控模型替身避免反复消耗 API 额度，但 CSV 工具、关键词 Retriever、Dispatcher 和主编排器仍执行真实项目代码。

## 主要文件

```text
BatteryMind/
├─ scripts/
│  ├─ run_batterymind.py       # 统一 CLI 入口
│  ├─ inspect_csv.py           # CSV 读取与基础字段检查
│  └─ quality.py               # 数据质量规则
├─ src/batterymind/
│  ├─ app.py                   # 当前统一编排器
│  ├─ llm_client.py            # 百炼 OpenAI-compatible 模型边界
│  ├─ llm_router.py            # 结构化模型路由
│  ├─ decisions.py             # RouterDecision 校验
│  ├─ tooling.py               # Tool Schema、白名单和 Dispatcher
│  ├─ real_tool_agent.py       # 独立 API 原生 Function Calling 原型
│  └─ rag_baseline.py          # 小型本地关键词检索基线
├─ data/knowledge/
│  └─ battery_knowledge.json   # 自建小词条，仅用于验证检索接口
└─ tests/                      # 单元测试与主链垂直切片测试
```

## 从这个项目真正学到什么

- LLM 只负责生成文本或提出结构化决定，不能亲自执行本地 Python 工具；
- Tool Schema、模型提出调用、Python 执行、Observation 回传是四个不同动作；
- 稳定的输入输出合同、白名单、失败 Guard 和测试比“成功回答一次”更重要；
- Trace 应记录实际发生的步骤，不能把独立原型拼成一条不存在的主链；
- 关键词检索可以验证接口，却不能替代真实向量 RAG 和检索评测。

## 项目状态

本仓库作为第一阶段学习成果保留，不再继续增加 Embedding、LangGraph、SOH 或部署章节。正式的第二项目将使用独立仓库，围绕真实公开电池数据、可复现 SOH 模型、真实文档知识库、向量检索、API 原生 Tool Calling 和端到端评测建设。
