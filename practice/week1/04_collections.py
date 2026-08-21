"""练习 04：list、set、dict 在字段检查中的分工。"""

# list 保留顺序和重复值，适合展示原始列名。
raw_columns = ["battery_id", "cycle", "voltage", "cycle"]

# set 自动去重，支持集合差集，适合比较“缺了哪些字段”。
required_columns = {"battery_id", "cycle", "capacity"}
actual_columns = set(raw_columns)
missing_columns = required_columns - actual_columns

# dict 用键说明每一份结果的含义，后面可以直接转换成 JSON。
profile = {
    "raw_columns": raw_columns,
    "required_columns": sorted(required_columns),
    "actual_columns": sorted(actual_columns),
    "missing_columns": sorted(missing_columns),
}

print("原始 list：", raw_columns)
print("转成 set 后：", actual_columns)
print("集合差集：", missing_columns)
print("结构化 profile：", profile)

# 唯一修改实验：在 raw_columns 中加入 capacity，预测 missing_columns。
