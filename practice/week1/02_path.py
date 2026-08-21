"""练习 02A：Path 最基础用法。

学习规则：
1. 先逐行读中文解释；
2. 运行一次；
3. 只修改 TARGET_NAME，再运行；
4. 不需要抄写整份代码。

请在 BatteryMind 项目根目录运行：
    python practice/week1/02_path.py
"""

# pathlib 是 Python 自带的路径工具模块。
# Path 是 pathlib 里面专门表示“文件或文件夹路径”的类。
from pathlib import Path


# Path("tests") 创建一个 Path 对象，表示项目根目录下的 tests。
# 后面的 / 不是数学除法；Path 使用 / 来拼接下一层路径。
# 这一整句最终表示 tests/fixtures/week1 文件夹。
fixture_dir = Path("tests") / "fixtures" / "week1"

# TARGET_NAME 是普通字符串，表示我们想检查的文件名。
# 练习时只改这一行，其他代码不重复写。
TARGET_NAME = "valid.csv"

# 一个 Path 可以继续和字符串用 / 拼接。
# target_path 最终表示 tests/fixtures/week1/valid.csv。
target_path = fixture_dir / TARGET_NAME

# print() 把括号中的内容显示在终端。
print("路径对象：", target_path)

# type() 查看变量属于什么类型；这里应看到 pathlib.Path 的具体实现类型。
print("对象类型：", type(target_path))

# .name 是属性，取得路径最后面的文件名，因此没有括号。
print("文件名 name：", target_path.name)

# .suffix 是属性，取得文件扩展名，例如 .csv。
print("后缀 suffix：", target_path.suffix)

# .parent 是属性，取得当前路径的上一层文件夹。
print("上一级 parent：", target_path.parent)

# .exists() 是方法，执行“这个路径是否存在”的检查，返回 True 或 False。
print("是否存在 exists()：", target_path.exists())

# .is_file() 检查路径存在时，它是不是普通文件。
print("是不是文件 is_file()：", target_path.is_file())

# .is_dir() 检查路径存在时，它是不是文件夹。
print("是不是文件夹 is_dir()：", target_path.is_dir())

# 文件不存在时调用 stat() 会报错，因此先用 if 判断 exists()。
if target_path.exists():
    # .stat() 取得文件状态，.st_size 再取得字节大小。
    print("文件大小：", target_path.stat().st_size, "字节")
else:
    # 路径不存在时执行这一条分支，不继续读取文件大小。
    print("路径不存在，所以不能读取文件大小。")


# 唯一修改练习：
# 依次把 TARGET_NAME 改成 empty.csv、wrong_extension.txt、not_exists.csv。
# 每次运行前，先预测 suffix、exists()、is_file() 和文件大小。
