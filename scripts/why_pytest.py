"""在学习 pytest 前，先看懂“测试”本身是什么。

运行方式（可以在 BatteryMind 项目根目录运行，也可以使用 VS Code 的运行按钮）：

    python scripts\why_pytest.py

这个文件没有使用 pytest。它只用普通 Python 完成三件事：
1. 调用 BatteryMind 的真实函数；
2. 得到实际结果；
3. 用 assert 检查实际结果是否等于预期结果。

pytest 后面做的核心事情并没有变。它只是替我们自动寻找、运行很多条
这样的检查，并把通过或失败统一汇总出来。
"""

from pathlib import Path

# 当前文件和 inspect_csv.py 位于同一个 scripts 文件夹。
# 当我们直接运行这个文件时，Python 会从当前脚本所在文件夹寻找模块，
# 因此这里直接写 inspect_csv，不再重复写 scripts.inspect_csv。
from inspect_csv import load_csv


# __file__ 是当前文件 scripts/why_pytest.py 的路径。
# parents[1] 回到 BatteryMind 项目根目录。
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 这是本次检查要交给真实业务函数的输入。
CSV_PATH = PROJECT_ROOT / "tests" / "fixtures" / "week1" / "valid.csv"

# Act（执行）：真正调用项目里的 load_csv，而不是伪造一个结果。
dataframe = load_csv(CSV_PATH)

# actual 是程序实际算出的结果；expected 是我们事先承诺的正确结果。
actual_shape = dataframe.shape
expected_shape = (3, 5)

# 故障实验（学到网站 10.2 时再做）：
# 取消下一行开头的 #，错误预期会覆盖上面的正确预期。
# expected_shape = (5, 3)
# 运行后观察 AssertionError；实验结束后重新加回 #，项目就恢复正确。

print(f"实际结果：{actual_shape}")
print(f"预期结果：{expected_shape}")

# assert 是 Python 自带的检查语句，不是 pytest 发明的。
# 条件为 True 就继续；条件为 False 就抛出 AssertionError。
assert actual_shape == expected_shape, (
    f"检查失败：实际形状 {actual_shape}，但预期形状是 {expected_shape}"
)

print("检查通过：load_csv 读取 valid.csv 后得到 3 行、5 列。")
