"""练习 07：Pandas 的一次成功、一次报错、一次修复。

本节还没有正式学习 main() 和 __name__，所以本文件暂时不使用它们。
代码按照从上到下的顺序直接执行，避免提前引入新语法。
"""

# Path 表示文件路径；pandas 负责读取 CSV。
from pathlib import Path
import pandas as pd


# fixture_dir 表示第 1 周样例数据所在的文件夹。
fixture_dir = Path("tests/fixtures/week1")

# 第一次保持 valid.csv；第二次只改成 missing_capacity.csv。
CSV_NAME = "missing_capacity.csv"

# 第一次选择 capacity；遇到 KeyError 后再根据 columns 选择实际存在的列。
SELECTED_COLUMN = "voltage"

# 使用 / 把文件夹路径和文件名拼起来。
csv_path = fixture_dir / CSV_NAME

# read_csv 读取 CSV，返回 DataFrame。
dataframe = pd.read_csv(csv_path)

# 先显示输入和表结构，后面发生错误时才能根据证据判断原因。
print("正在读取：", csv_path)
print("shape：", dataframe.shape)
print("columns：", dataframe.columns.tolist())

# 单个字符串选择一列，结果通常是 Series。
# 如果 SELECTED_COLUMN 不在 columns 中，这一行会产生 KeyError。
selected_series = dataframe[SELECTED_COLUMN]

print("选择的列：", SELECTED_COLUMN)
print(selected_series)
print("结果类型：", type(selected_series))


# 学习顺序：
# 1. 默认配置运行成功；
# 2. 只把 CSV_NAME 改成 missing_capacity.csv，复现 KeyError；
# 3. 根据 columns，只把 SELECTED_COLUMN 改成 voltage，恢复成功；
# 4. 最后恢复默认配置。
