# BatteryMind

面向电池实验数据质量检查、SOH 预测、知识检索和智能诊断的学习型项目。

## 当前阶段

Week 0：环境和仓库初始化。

## 环境

- Windows
- Python 3.11
- Conda environment: batterymind

## 快速运行

```powershell
conda activate batterymind
python -m pip install -r requirements.txt
python scripts\hello_batterymind.py
```

## 当前输出

检查项目路径、Python 环境和 Pandas 安装状态。
```

`docs\debug-log.md` 写入：

```md
# Debug Log

## 记录格式

- 日期：
- 执行命令：
- 完整错误：
- 原因：
- 解决方法：
- 如何避免再次发生：
```

你在学习什么：README 是别人运行项目的入口；debug log 是你积累排错能力的证据。

`docs\decisions\ADR-000-project-scope.md` 写入：

```md
# ADR-000：BatteryMind 第一版项目范围

## 真实问题

电池实验数据来自不同文件和实验批次，存在格式、缺失、异常和难以复现的问题。第一版先解决数据读取与质量检查。

## 最简单方案

用 Python 和 Pandas 读取一份真实 CSV，输出字段、行数、缺失值和基本统计。

## 暂时不引入

- 不使用数据库；
- 不使用 Spark；
- 不使用 RAG、Agent 或 MCP；
- 不做复杂网页。

原因：第 0 周还没有证据说明这些技术是必要的。

## 验收

一条命令能运行环境检查；下一阶段一条命令能读取真实数据并输出质量摘要。
```

`docs\weekly\week-00.md` 写入：

```md
# Week 00

## 本周要解决的问题

先让 BatteryMind 拥有可运行、可追踪的项目骨架。

## 我亲自完成的内容

- 创建 Conda 环境；
- 创建仓库和目录；
- 运行环境检查脚本；
- 完成第一次 Git 提交。

## 我为什么没有加入复杂技术

当前还没有真实数据问题和指标证明它们有必要。先建立最小可运行版本。

## 证据

- 运行命令：`python scripts\hello_batterymind.py`
- Git commit：填写实际 commit id
- 遇到的错误：填写到 `docs\debug-log.md`