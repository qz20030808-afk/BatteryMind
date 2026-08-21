"""练习 02B（扩展）：读懂 __file__、resolve()、parent 和 parents。

这一份不是 read_csv 的前置要求。先完成 02_path.py，再用本文件
理解真实项目为什么经常从“当前代码文件的位置”寻找项目根目录。
"""

# 从 Python 自带的 pathlib 模块导入 Path 类。
from pathlib import Path


# __file__ 是 Python 提供的特殊变量，表示“当前这份 .py 文件的路径”。
# Path(__file__) 把这个路径字符串转换成 Path 对象。
current_file = Path(__file__)

# resolve() 把路径整理成完整的绝对路径。
# 例如它会变成 C:/Users/.../BatteryMind/practice/week1/02b_path_project_root.py。
absolute_file = current_file.resolve()

# parent 表示直接上一级。
# 当前文件的上一级是 practice/week1 文件夹。
week1_dir = absolute_file.parent

# parents 保存所有祖先目录，并且从 0 开始计数：
# parents[0] 是 week1，parents[1] 是 practice，parents[2] 是 BatteryMind。
project_root = absolute_file.parents[2]

# 从项目根目录开始，使用 / 逐层拼出 valid.csv 的绝对路径。
csv_path = project_root / "tests" / "fixtures" / "week1" / "valid.csv"

# 下面逐项打印，目的是让抽象关系变得可见。
print("__file__ 的原始值：", __file__)
print("Path(__file__)：", current_file)
print("resolve() 后：", absolute_file)
print("parent：", week1_dir)
print("parents[0]：", absolute_file.parents[0])
print("parents[1]：", absolute_file.parents[1])
print("parents[2]：", absolute_file.parents[2])
print("项目根目录：", project_root)
print("最终 CSV 路径：", csv_path)
print("CSV 是否存在：", csv_path.exists())


# 本文件只观察，不要求修改。
# 最终只需能画出：当前文件 → week1 → practice → BatteryMind。
