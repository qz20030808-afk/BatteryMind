"""练习 01：变量、类型与 f-string。

不要抄写整份文件。第一次直接运行；第二次只修改下方两个学习变量。
"""

# 变量 = 给一个值起名字。右边先产生值，再把值交给左边的名字。
csv_path = "tests/fixtures/week1/valid.csv"
required_column_count = 3

# f-string 会把大括号中的变量值放进最终字符串。
message = f"准备检查 {csv_path}，最少需要 {required_column_count} 个字段"

print("csv_path 的值：", csv_path)
print("csv_path 的类型：", type(csv_path))
print("required_column_count 的值：", required_column_count)
print("required_column_count 的类型：", type(required_column_count))
print("最终消息：", message)

# 唯一修改实验：把 required_column_count 改成 5，再预测最终消息。
