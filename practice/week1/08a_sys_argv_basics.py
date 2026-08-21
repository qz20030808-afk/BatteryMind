"""练习 08a：先看见“命令行参数”进入 Python 后的原始样子。

请从 BatteryMind 项目根目录运行：
python practice/week1/08a_sys_argv_basics.py hello 123

这一整行叫“命令”：
- python：要启动的程序。
- practice/week1/08a_sys_argv_basics.py：交给 Python 执行的脚本。
- hello 和 123：启动脚本时额外交给它的两个命令行参数。

这不是正式项目的推荐写法。它只帮助你理解 argparse 的输入来自哪里。
"""

# sys 是 Python 自带的标准库模块，提供与 Python 运行环境有关的信息。
import sys


# sys.argv 是一个列表，保存运行命令中的脚本名和额外参数。
# argv 是 argument vector 的缩写，可以先理解为“参数列表”。
print("完整的 sys.argv：", sys.argv)

# 第 0 项通常是正在运行的脚本路径，不是我们额外传入的业务参数。
print("sys.argv[0]（脚本路径）：", sys.argv[0])

# 命令末尾的 hello 是第一个额外参数，所以索引是 1。
print("sys.argv[1]（第一个额外参数）：", sys.argv[1])

# 命令末尾的 123 是第二个额外参数，所以索引是 2。
# 注意：即使它看起来像数字，原始命令行参数仍然是字符串。
print("sys.argv[2]（第二个额外参数）：", sys.argv[2])
print("sys.argv[2] 的类型：", type(sys.argv[2]))


# 运行后请回答：
# 1. hello 为什么位于索引 1，而不是索引 0？
# 2. 123 的类型为什么仍是字符串？
# 3. 如果用户忘记输入 123，直接访问 sys.argv[2] 会发生什么？
#
# 这三个麻烦正是 argparse 要帮助正式项目解决的一部分：
# 它会按名字声明参数、检查是否缺失、转换基础类型，并生成统一帮助信息。
