"""练习 09B：用真实路径理解 dict、JSON、if 和退出码。

这个文件是一个完整的最小程序：
1. 调用者从命令行传入一个 CSV 路径。
2. 程序检查路径是否指向真实文件。
3. 程序把检查结果先组织成 Python 字典。
4. 程序把字典转换成 JSON，输出给人或其他程序。
5. 程序用退出码告诉操作系统这次执行成功还是失败。

请从 BatteryMind 根目录分别运行：
python practice/week1/09b_json_and_exit_code.py tests/fixtures/week1/valid.csv
python practice/week1/09b_json_and_exit_code.py tests/fixtures/week1/not_exists.csv
"""

# argparse 读取调用者写在命令后面的真实路径。
from argparse import ArgumentParser

# json 把 Python 字典转换成 JSON 文本。
import json

# sys.exit() 在程序结束时把退出码交给操作系统。
import sys

# Path 把路径文字转换成可以执行 exists()、is_file() 等检查的对象。
from pathlib import Path


# parser 保存“这个程序接受什么命令行参数”的规则。
parser = ArgumentParser(description="检查一个 CSV 路径，并输出 JSON 结果")

# input_csv 是位置参数的名字。
# 调用者传入的实际路径会被 type=Path 转换成 Path 对象。
parser.add_argument("input_csv", type=Path, help="准备检查的 CSV 文件路径")

# parse_args() 读取 sys.argv，并返回解析结果对象。
# parsed_arguments 是我们自己起的变量名；也可以叫 args。
parsed_arguments = parser.parse_args()

# 从解析结果中取出调用者真正传入的路径。
csv_path = parsed_arguments.input_csv


# if 不是循环。它只根据条件选择一个分支执行一次。
# 这里检查的是调用者传入的真实路径，不再使用手工设置的 MODE。
if csv_path.exists() and csv_path.is_file():
    # result 是 Python 字典，用稳定的键保存一次成功检查的多个结果。
    # 字典留在 Python 程序内部，后面还要转换成 JSON 才方便跨程序传递。
    result = {
        "ok": True,
        "file": str(csv_path),
        "message": "输入路径存在，并且是文件",
    }

    # 退出码 0 是通用约定，表示程序成功完成。
    exit_code = 0
else:
    # 失败时仍使用相同的 result 变量，但保存错误相关字段。
    # ok、error_type、message 是给调用者读取的稳定字段名。
    result = {
        "ok": False,
        "file": str(csv_path),
        "error_type": "FileNotFoundError",
        "message": "输入路径不存在，或者它不是文件",
    }

    # 非 0 退出码表示失败。本练习用 1 表示一般失败。
    exit_code = 1


# json.dumps() 把 Python dict 序列化成 JSON 格式的字符串。
# JSON 不是只能记录错误；上面的成功结果也会被转换成 JSON。
json_text = json.dumps(result, ensure_ascii=False, indent=2)

# print() 把 JSON 文字写到标准输出 stdout。
# PowerShell 会显示它，其他程序也可以捕获并解析它。
print(json_text)

# sys.exit() 结束程序，并把 exit_code 交给操作系统。
# 这不是“调用 JSON”；JSON 负责详细信息，退出码只负责成功/失败状态。
sys.exit(exit_code)


# 在 PowerShell 中，上一条外部程序的退出码保存在 $LASTEXITCODE 中。
# 每次运行本文件后，可以紧接着输入：
# $LASTEXITCODE
