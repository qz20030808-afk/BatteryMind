"""Pandas 衔接 A：从 Python 列表/字典走到 Series 和 DataFrame。"""

import pandas as pd


# 普通 Python 字典：键像列名，列表像一整列数据。
battery_data = {
    "battery_id": ["B001", "B001", "B002"],
    "cycle": [1, 2, 1],
    "capacity": [2.00, 1.98, 2.05],
}

print("1. 普通字典中的 capacity 列")
print(battery_data["capacity"])
print(type(battery_data["capacity"]))


# Series：一列带索引、名称和数据类型的数据。
capacity_series = pd.Series(battery_data["capacity"], name="capacity")

print("\n2. Pandas Series")
print(capacity_series)
print("类型：", type(capacity_series))
print("列名：", capacity_series.name)
print("数据类型：", capacity_series.dtype)


# DataFrame：多列组成的二维表格。
df = pd.DataFrame(battery_data)

print("\n3. Pandas DataFrame")
print(df)
print("类型：", type(df))
print("shape（行数, 列数）：", df.shape)
print("columns（列名）：", df.columns.tolist())
print("index（行索引）：", df.index.tolist())
print("dtypes（每列类型）：")
print(df.dtypes)


# 选择一列得到 Series；选择多列得到 DataFrame。
print("\n4. 选择一列和多列")
print("df['capacity'] 类型：", type(df["capacity"]))
print("df[['battery_id', 'capacity']] 类型：", type(df[["battery_id", "capacity"]]))
