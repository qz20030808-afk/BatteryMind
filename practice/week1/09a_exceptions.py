"""练习 09A：raise、try 和 except 的最小基础。"""

from pathlib import Path


# 练习时只改 FILE_NAME；先用 valid.csv，再改成 not_exists.csv。
FILE_NAME = "not_exists.csv"
csv_path = Path("tests/fixtures/week1") / FILE_NAME

# try 表示“尝试执行这段可能失败的代码”。
try:
    # 如果文件不存在，主动创建并抛出 FileNotFoundError。
    if not csv_path.exists():
        raise FileNotFoundError(f"文件不存在：{csv_path}")

    # 没有异常时，程序继续执行这里。
    print("检查成功：", csv_path)

# except 捕获指定类型的异常，并把异常对象保存为 error。
except FileNotFoundError as error:
    # str(error) 取得异常中的可读消息。
    print("检查失败：", str(error))


# 本文件为了观察而捕获异常；正式工具的底层函数可以 raise，
# 最外层入口再统一决定怎样输出 JSON 和退出码。
