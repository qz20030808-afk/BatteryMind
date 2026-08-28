# Week 2 Day4–7：BatteryMind Agent 核心地基复盘

> Day3 已完成并锁定。第一次真实模型调用从 Day4 的 16.1 开始，不要求回头修改 Day3 练习。

## 1. 我能画出的完整行动链

用户入口 → Agent 决策 → Tool Dispatcher → CSV/RAG/SOH 工具 → Observation → Verifier → 最终回答与 Trace。

请在学完 Day7 后，用自己的话改写上面一行，并给每层写出真实文件。

## 2. 两条必须能演示的路线

- 真实 Tool Calling 路线：问题 → qwen3.7-plus 返回 `tool_calls` → Dispatcher 执行 `inspect_battery_csv` → Observation → qwen3.7-plus 最终回答。
- 知识路线：问题 → retrieval → 带来源 chunk → 停止。

## 3. 真实 API 硬验收

以下三条都必须在配置 `DASHSCOPE_API_KEY` 后由你本人运行，缺 Key 或固定 mock 不算完成：

- `python -m practice.week2.05_model_boundary`：保存第一次真实 response id、content 与 usage，并能解释请求与响应各字段来自哪里。
- `python -m practice.week2.06_structured_decision`：保存模型原始 JSON 与校验后 decision。
- `python -m practice.week2.07_tool_calling`：保存 tool_call、Observation 与第二次模型回答。

## 4. 一个失败案例

记录你实际运行过的未知工具、缺文件、空检索或最大步数停止案例：

> 待填写。

## 5. 两分钟面试表达

按“问题—设计—执行链—真实 API 证据—自动测试证据—当前边界—下一步改进”写。在你完成在线硬验收前，只能说“已实现真实 API 代码并通过 mock 边界测试”，不能说“已跑通线上 Agent”；关键词基线也不能说成向量 RAG。

> 待填写。
