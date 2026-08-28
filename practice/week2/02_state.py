"""Day2 · 14.3：字典状态与 if 分支。

运行位置：BatteryMind 项目根目录
运行命令：python practice/week2/02_state.py

今天的 state 只是普通 Python dict，不是 LangGraph 对象。
学习目标是看懂：输入怎样进入字典，条件怎样产生 True/False，
以及 if/else 怎样修改同一个 state。
"""


def choose_route(question):
    """根据当前的简单关键词规则，返回一份完整状态。"""

    # 创建一个 dict，并让变量 state 指向它。
    # question 键先保存本次输入；route 和 reason 先用空字符串占位。
    state = {
        "question": question,
        "route": "",
        "reason": "",
    }

    # state["question"] 从字典中读取问题字符串。
    # 两个 in 判断分别得到 True 或 False。
    # or 表示只要其中一个判断是 True，整个条件就是 True。
    if "电池" in state["question"] or "容量" in state["question"]:
        # 条件为 True 时，只执行这个缩进块。
        # "search" 只是路线标签；它不会在这里自动执行搜索。
        state["route"] = "search"
        state["reason"] = "问题涉及电池知识"
    else:
        # 条件为 False 时，跳过上面的缩进块，只执行这里。
        state["route"] = "direct"
        state["reason"] = "当前关键词规则认为不需要查询电池知识"

    # 把修改完成的整个 dict 交回调用位置。
    return state


# 先运行电池问题，观察 if 路线。
first_question = "电池容量为什么会下降？"
first_result = choose_route(first_question)
print("输入：", first_question)
print("状态：", first_result)
print("-" * 40)

# 再运行普通问候，观察 else 路线。
# 今天故意不用 for 循环；循环会放到 Day3 从基础开始学习。
second_question = "你好"
second_result = choose_route(second_question)
print("输入：", second_question)
print("状态：", second_result)
