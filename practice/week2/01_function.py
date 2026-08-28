"""Day2 · 14.2：函数、参数、调用与 return。

运行位置：BatteryMind 项目根目录
运行命令：python practice/week2/01_function.py

学习目标不是背语法，而是追踪一条完整数据流：
两个输入 -> 函数形参 -> 函数生成结果 -> return -> result -> print
"""


def build_question(battery_id, symptom):
    """把电池编号和症状组合成后续模块可以处理的问题。"""

    # battery_id 和 symptom 是形参。
    # 调用函数时传入的两个值，会按位置分别交给它们。
    question = f"请分析电池 {battery_id} 的问题：{symptom}"

    # return 不负责把文字显示到终端。
    # 它会结束本次函数调用，并把 question 的值交回调用位置。
    return question


# 这两个变量模拟 BatteryMind 从用户界面收到的两项输入。
battery_id = "B001"
symptom = "容量下降"

# 等号右边先执行：调用 build_question，并取得它 return 的字符串。
# 等号左边后保存：result 最终保存返回的字符串。
result = build_question(battery_id, symptom)

# print 只负责让人看见结果；后续程序真正使用的是 result 变量。
print("输入 1：", battery_id)
print("输入 2：", symptom)
print("函数返回：", result)
