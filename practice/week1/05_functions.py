"""练习 05：参数、return、调用者与可复用函数。"""


def find_missing_columns(
    required_columns: set[str],
    actual_columns: set[str],
) -> list[str]:
    """接收必需字段和实际字段，返回排序后的缺失字段。"""
    missing_columns = required_columns - actual_columns
    return sorted(missing_columns)


required = {"battery_id", "cycle", "capacity"}
actual = {"battery_id", "cycle", "voltage"}

# 函数调用：两个实际值交给两个参数，返回值再存入 result。
result = find_missing_columns(required, actual)
print("缺失字段：", result)

# 唯一修改实验：给 actual 加上 capacity，再预测 result。
# 可选理解实验：把 return 那一行临时注释，观察 result 为什么变成 None；随后恢复。
