# BatteryMind

> 一个从“可靠读取电池实验数据”开始，逐步扩展到数据质量分析、SOH 预测、RAG 检索和诊断 Agent 的学习型工程项目。

## 1. 项目背景

电池实验数据常来自不同设备、批次和导出流程。进入分析或 AI 流程前，文件可能已经存在这些问题：

- 路径写错或文件不存在；
- 把文件夹、空文件或其他格式误当成 CSV；
- 表格缺少 `battery_id`、`cycle`、`capacity` 等核心字段；
- 输入问题一直传到特征工程、模型或 Agent 层，最后才以难定位的错误暴露。

BatteryMind 的第一步不是直接调用大模型，而是先建立一个可测试的确定性数据入口。它负责尽早拒绝非法输入，并为后续 Pandas 分析、SOH 预测、RAG 和 Agent 工具调用提供稳定的数据契约。

## 2. 当前版本解决什么问题

当前完成的是第 1 周版本：**CSV 输入检查器**。

它已经能够：

1. 使用 `pathlib.Path` 检查输入是否存在、是否为普通文件、后缀是否为 `.csv`、文件是否为空；
2. 使用 Pandas 读取 CSV，并拒绝只有表头、没有数据行的表格；
3. 检查 `battery_id`、`cycle`、`capacity` 三个核心字段是否缺失；
4. 使用 pytest 自动验证正常文件、缺列、缺文件、错后缀、空文件和目录输入等边界；
5. 通过独立练习程序验证 JSON 结构化输出与退出码的成功/失败行为。

当前还不是完整的 AI Agent。更准确的描述是：**它正在成为未来 Agent 可以调用的可靠数据工具**。

## 3. 当前行动链

```text
外部 CSV 路径
    ↓
Path 输入检查
    ↓
Pandas 读取为 DataFrame
    ↓
核心字段契约检查
    ↓
终端结果 / 自动测试证据
```

下一步会把已练习的命令行参数、JSON 输出和退出码正式接入主脚本，使其他程序可以传入任意 CSV，并稳定判断成功或失败。

## 4. 项目结构

```text
BatteryMind/
├─ scripts/
│  ├─ inspect_csv.py          # 当前主业务模块：路径检查、CSV 读取、字段检查
│  └─ why_pytest.py           # 不依赖 pytest 的最小测试原理演示
├─ practice/week1/
│  └─ 09b_json_and_exit_code.py  # JSON 与退出码的完整最小练习
├─ tests/
│  ├─ fixtures/week1/         # 可重复使用的正常与异常 CSV 样例
│  ├─ test_inspect_csv.py     # 主业务模块的 6 条自动测试
│  └─ test_week1_practice_cli.py # JSON/退出码练习的 2 条 CLI 测试
├─ docs/                      # 决策、调试和周复盘文档
├─ requirements.txt           # 当前 Python 依赖及版本
└─ README.md                  # 项目入口：背景、运行方法、证据和边界
```

## 5. 技术选择与当前掌握深度

| 技术 | 当前在项目里负责什么 | 当前阶段 | 后续如何继续深化 |
| --- | --- | --- | --- |
| Python 3.11 | 函数、异常、模块导入与业务流程 | 已用于真实项目基础逻辑，不等于“精通 Python” | 类型设计、包结构、API、异步调用、Agent 工具层 |
| pathlib | 构造和验证跨平台文件路径 | 已接入主脚本 | 数据集目录、模型文件、索引与配置路径管理 |
| Pandas | 读取 CSV、查看形状与字段、判断空表 | 入门工程使用 | 缺失值、重复值、异常值、分组、合并、时序特征和性能优化 |
| JSON | 把 Python 字典变成跨程序可读的结构化文本 | 已在独立练习中验证，尚未接入主脚本 | CLI/API 返回契约、Pydantic 校验、RAG 与 Agent tool result |
| pytest | 自动重放正常和异常场景 | 已覆盖 8 条检查 | fixture、参数化、mock、覆盖率、集成测试和 Agent 评测 |

技术栈不是“上过一次课”的清单。只有当某项技术在项目中承担明确职责，并且有代码和测试证据时，才适合写进项目描述；面试时还要如实说明当前深度。

## 6. 环境准备

### 文件在哪里

本项目根目录：

```text
C:\Users\qiuzhe\Desktop\work\BatteryMind
```

下面所有命令默认都从这个目录运行。

### 进入项目并确认解释器

```powershell
conda activate batterymind
Set-Location -LiteralPath 'C:\Users\qiuzhe\Desktop\work\BatteryMind'
python -c "import sys; print(sys.executable)"
```

最后一条应指向：

```text
D:\Anaconda\envs\batterymind\python.exe
```

若输出的是 `D:\Python\python.exe`，说明当前运行入口使用了另一套 Python。先切换解释器，不要盲目重复安装依赖。

### 安装依赖

```powershell
python -m pip install -r requirements.txt
```

## 7. 运行当前主脚本

### 运行哪个文件

- 代码位置：`scripts/inspect_csv.py`
- 文件类型：可被导入的业务模块，同时提供当前演示入口
- 正确运行者：当前 `batterymind` 环境中的 Python
- 从哪里运行：BatteryMind 根目录

### 运行命令

```powershell
python -m scripts.inspect_csv
```

当前演示会读取 `tests/fixtures/week1/valid.csv`，预期看到：

```text
读取文件：valid.csv
DataFrame 形状：(3, 5)
实际字段：['battery_id', 'cycle', 'capacity', 'voltage', 'temperature']
缺失核心字段：[]
```

`缺失核心字段：[]` 表示三个必需字段全部存在。当前主入口仍使用项目内固定样例；接收任意路径的命令行入口将在下一步接入。

## 8. 运行 JSON 与退出码练习

### 运行哪个文件

- 代码位置：`practice/week1/09b_json_and_exit_code.py`
- 文件类型：完整的命令行练习程序
- 正确运行者：当前 Python 直接运行这个文件
- 从哪里运行：BatteryMind 根目录

成功输入：

```powershell
python practice\week1\09b_json_and_exit_code.py tests\fixtures\week1\valid.csv
$LASTEXITCODE
```

程序会输出 `"ok": true`，随后 `$LASTEXITCODE` 应为 `0`。

失败输入：

```powershell
python practice\week1\09b_json_and_exit_code.py tests\fixtures\week1\not_exists.csv
$LASTEXITCODE
```

程序会输出 `"ok": false` 和 `"error_type": "FileNotFoundError"`，随后 `$LASTEXITCODE` 应为 `1`。

JSON 提供详细结果，退出码只向操作系统说明本次运行成功还是失败；二者职责不同。

## 9. 运行自动测试

### 测试文件由谁运行

`tests/test_inspect_csv.py` 和 `tests/test_week1_practice_cli.py` 是测试集合，应由 pytest 收集和执行。不要把它们当普通脚本点击“运行 Python 文件”。

### 运行命令

```powershell
python -m pytest -q
```

当前预期结果：

```text
8 passed
```

这证明当前实现通过了已经写下的 8 条检查；它不代表所有未知输入都正确，也不代表未来 Agent 的回答质量已经得到验证。

## 10. 设计取舍

### 为什么先做确定性数据工具

Agent 的决策依赖工具和输入。若底层数据入口不稳定，上层模型只会把错误包装得更复杂。先把可预测、可测试的部分固定下来，后续才能分别判断是数据工具失败、检索失败，还是 Agent 决策失败。

### 为什么暂时不用 Spark、数据库或 Agent 框架

当前数据量和需求还不足以证明这些依赖的必要性。先用 Python、Path 和 Pandas 建立最小可运行链路，更容易理解、测试和迭代；出现真实规模瓶颈后再升级架构。

## 11. 当前限制

- 主脚本还不能从命令行接收任意 CSV 路径；
- JSON 与退出码尚未正式整合进 `scripts/inspect_csv.py`；
- 目前只检查路径、空表和必需字段，还没有分析缺失值、重复值、异常值和电池时序一致性；
- 尚未实现 SOH 模型、RAG 知识库、Agent 编排和对应评测；
- 当前样例数据很小，还没有大文件性能证据。

## 12. 后续路线

1. 把 argparse、JSON 和退出码接入主脚本，形成稳定 CLI 契约；
2. 使用 Pandas 完成缺失、重复、异常和分组时序检查，输出数据质量报告；
3. 构建 SOH 特征与可复现的基线模型，并记录指标；
4. 为电池资料和数据字典建立 RAG 检索链，加入固定问题集和检索评测；
5. 将数据检查、检索和诊断封装成 Agent tools，评测工具选择、任务成功率、延迟和成本；
6. 用真实比赛、企业命题或用户反馈补充外部验收证据。

## 13. 面试时的 30 秒说明

> BatteryMind 面向电池实验数据进入 AI 流程前的质量问题。我先用 Python、Path 和 Pandas 做了可测试的 CSV 输入检查器，对缺文件、空文件、错后缀、目录输入和核心字段缺失进行前置拦截，并用 pytest 固化了 8 条正常与异常检查。当前它是未来 Agent 可调用的确定性工具，还没有包装成完整 Agent；下一步会接入结构化 CLI、数据质量分析，再扩展到 RAG、工具调用和效果评测。
