"""练习 03：用 if/elif/else 表达路径检查规则。"""

# 导入 Path 类，让路径可以使用 exists()、suffix、stat() 等功能。
from pathlib import Path


# 先用最基础的相对路径表示样例文件夹。
# 本周所有命令都从 BatteryMind 根目录运行，所以这个相对路径有效。
fixture_dir = Path("tests") / "fixtures" / "week1"

# 字典把容易记的案例名称映射到实际文件名。
CASES = {
    "valid": "valid.csv",
    "not_found": "not_exists.csv",
    "wrong_extension": "wrong_extension.txt",
    "empty": "empty.csv",
}

# 练习时只修改 CASE，不重复改完整路径。
CASE = "not_found"

# CASES[CASE] 根据案例名找到文件名，再和 fixture_dir 拼接。
csv_path = fixture_dir / CASES[CASE]

# f-string 把案例名和文件名放进提示消息。
print(f"当前案例：{CASE}，路径：{csv_path}")

# not 把 exists() 的结果取反：不存在时条件为 True。
if not csv_path.exists():
    print("检查失败：文件不存在")
# 前面不存在的情况已经排除，现在检查它是否为普通文件。
elif not csv_path.is_file():
    print("检查失败：路径不是文件")
# lower() 统一成小写，避免 .CSV 和 .csv 大小写不同。
elif csv_path.suffix.lower() != ".csv":
    print("检查失败：文件后缀不是 .csv")
# 前面已经证明文件存在，所以现在可以安全调用 stat()。
elif csv_path.stat().st_size == 0:
    print("检查失败：文件为空")
# 前面的失败条件都不成立，才进入成功分支。
else:
    print("检查成功：路径基础检查通过")
