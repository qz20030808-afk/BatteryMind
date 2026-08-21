"""Pandas 衔接 B：用最基础路径学习 read_csv。

本文件故意暂时不用 __file__、resolve() 和 parents，避免在学习 read_csv
时同时引入太多概念。请从 BatteryMind 项目根目录运行。
"""

# 从 Python 自带的 pathlib 模块导入 Path 类。
from pathlib import Path

# 导入 pandas，并按照惯例给它一个短名字 pd。
import pandas as pd


# 普通字符串表示路径文字；Path(...) 把它变成路径对象。
# 因为从 BatteryMind 根目录运行，所以 tests/... 是正确的相对路径。
csv_path = Path("tests/fixtures/week1/valid.csv")

# 读取前先打印路径，确认程序准备读取哪个文件。
print("准备读取：", csv_path)

# exists() 检查路径是否真实存在，结果是 True 或 False。
print("文件是否存在：", csv_path.exists())

# pd.read_csv(...) 打开并解析 CSV，然后返回一个 DataFrame。
# 等号把返回的 DataFrame 保存到 dataframe 变量。
dataframe = pd.read_csv(csv_path)

# type() 用来确认读取结果确实是 DataFrame。
print("读取结果类型：", type(dataframe))

# shape 是属性，返回 (行数, 列数)，所以后面没有括号。
print("表格形状：", dataframe.shape)

# columns 先得到 Pandas 的列名 Index；tolist() 再转成普通 Python 列表。
print("所有列名：", dataframe.columns.tolist())

# head() 是方法，执行“返回前 5 行”的动作，所以需要括号。
print("前 5 行：")
print(dataframe.head())


# 唯一修改练习：
# 把 valid.csv 改成 missing_capacity.csv，预测 shape 和 columns 的变化。
