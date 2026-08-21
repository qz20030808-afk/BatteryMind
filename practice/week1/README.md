# Week 1 练习文件地图

这些文件已经预先创建。学习时不需要反复运行 `New-Item` 或复制整段代码，只需要按学习站指引打开、运行和修改。

| 文件 | 用途 | 你主要做什么 |
|---|---|---|
| `01_variables.py` | 变量、类型和 f-string | 只改字段数量，预测消息 |
| `02_path.py` | `Path` 基础 | 每行有解释；只改 `TARGET_NAME` 比较四类路径 |
| `02b_path_project_root.py` | Path 工程扩展 | 单独理解 `__file__`、`resolve()`、`parent/parents`，只观察不修改 |
| `03_conditions.py` | 条件判断 | 只改 `CASE`，走过四条分支 |
| `04_collections.py` | list、set 和 dict | 只加一个字段，预测集合差集 |
| `05_functions.py` | 参数和返回值 | 只补一个实际字段，观察返回值 |
| `06a_pandas_table_and_dataframe.py` | 表格、Series、DataFrame | 看完结构课立即运行 |
| `06b_pandas_read_csv.py` | CSV 到 DataFrame | 看完读取课立即运行 |
| `06c_pandas_inspection.py` | 类型、缺失与统计 | 看完检查课立即运行 |
| `06_pandas_foundations.py` | 三段内容的完整复习 | 当天最后串联复习 |
| `07_pandas_exercises.py` | Pandas 修改实验 | 只修改 `CSV_NAME` 和 `SELECTED_COLUMN` |
| `08a_sys_argv_basics.py` | 命令行参数从哪里来 | 传入 `hello 123`，观察 `sys.argv` |
| `08_argparse_basics.py` | argparse 命令行接口基础 | 先看 `--help`，再传一次真实路径 |
| `09a_exceptions.py` | 异常基础 | 只改 `FILE_NAME`，比较成功与失败 |
| `09b_json_and_exit_code.py` | dict、JSON、stdout 与退出码 | 分别传入真实存在和不存在路径，再看 `$LASTEXITCODE` |
| `scripts/why_pytest.py` | pytest 前置桥梁 | 先看普通 Python 怎样完成“调用真实函数 + assert 核对结果” |
| `tests/test_inspect_csv.py` | pytest 与边界验收 | 不点“运行 Python 文件”；使用 `python -m pytest ...` 让 pytest 收集并运行六条核心测试 |

统一在项目根目录运行，例如：

```powershell
python practice\week1\06_pandas_foundations.py
```

学习原则：每个文件先读注释并预测，运行一次验证理解，再做一次最小修改。除非学习站明确要求，不重复创建文件、不重新抄写整段代码。

如果你已经学到后面的章节才发现前置知识缺口，以学习站当前章节中的“当前位置补课”为准，不需要返回旧章节重新学习。
