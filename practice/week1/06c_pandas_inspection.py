"""Pandas 衔接 C：检查列类型、缺失值与数字摘要。"""

# 导入 Path 和 pandas；两者分别负责表示路径和读取表格。
from pathlib import Path
import pandas as pd


# 使用已经学过的基础相对路径，不混入工程扩展语法。
csv_path = Path("tests/fixtures/week1/valid.csv")

# read_csv 返回 DataFrame，并保存到 dataframe。
dataframe = pd.read_csv(csv_path)

# dtypes 属性列出每一列的数据类型。
print("1. 每列的数据类型")
print(dataframe.dtypes)

# isna() 把每个单元格转换成“是否缺失”的 True/False。
missing_mask = dataframe.isna()
print("\n2. 每个单元格是否缺失")
print(missing_mask)

# 对布尔表调用 sum()，True 按 1 累加，得到每列缺失数量。
missing_count = missing_mask.sum()
print("\n3. 每列缺失值数量")
print(missing_count)

# select_dtypes(...) 选择数字类型列，避免对 battery_id 求平均数。
numeric_dataframe = dataframe.select_dtypes(include="number")

# describe() 对数字列生成计数、均值、标准差、最值和分位数。
numeric_summary = numeric_dataframe.describe()
print("\n4. 数字列基础统计")
print(numeric_summary)
