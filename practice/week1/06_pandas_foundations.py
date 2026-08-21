"""Pandas 基础串联复习：完成 06a、06b、06c 后再运行。

本文件只把已经分别学过的内容串起来，不引入新的路径语法。
"""

from pathlib import Path
import pandas as pd


csv_path = Path("tests/fixtures/week1/valid.csv")
dataframe = pd.read_csv(csv_path)

print("CSV 路径：", csv_path)
print("DataFrame 类型：", type(dataframe))
print("shape：", dataframe.shape)
print("columns：", dataframe.columns.tolist())
print("dtypes：")
print(dataframe.dtypes)
print("每列缺失数量：")
print(dataframe.isna().sum())
print("数字列摘要：")
print(dataframe.select_dtypes(include="number").describe())
