"""练习 08：argparse 最小基础。

本文件在 9.2 第一次出现，不要求你回到以前学习。
它只教一个位置参数，学完再把同样思路接入 inspect_csv.py。

argparse 是 Python 标准库里的命令行参数解析工具。
它读取 08a 中见过的 sys.argv，并把原始字符串按我们声明的规则整理好。
"""

# ArgumentParser 是 Python 标准库 argparse 中的命令行参数解析器。
from argparse import ArgumentParser

# Path 用来把用户输入的路径文字转换成路径对象。
from pathlib import Path


# 创建解析器；description 会显示在 --help 中。
parser = ArgumentParser(description="演示如何从命令行接收一个 CSV 路径")

# 声明一个名为 input_csv 的位置参数。
# “位置参数”表示调用者不写 --input_csv 这个名字，程序按它在命令中的位置识别。
# 例如命令末尾的 valid.csv 位于第 1 个业务位置，所以会放进 input_csv。
# type=Path 表示 argparse 收到文字后自动把它转换成 Path。
# help 说明这个参数的用途。
parser.add_argument(
    "input_csv",
    type=Path,
    help="准备检查的 CSV 文件路径",
)

# parse_args() 读取用户在命令后输入的内容，并返回参数对象。
args = parser.parse_args()

# args.input_csv 取得用户传入的 input_csv，类型已经是 Path。
csv_path = args.input_csv

print("收到的路径：", csv_path)
print("路径类型：", type(csv_path))
print("是否存在：", csv_path.exists())


# 先运行帮助：
# python practice/week1/08_argparse_basics.py --help
# 再传真实路径：
# python practice/week1/08_argparse_basics.py tests/fixtures/week1/valid.csv
