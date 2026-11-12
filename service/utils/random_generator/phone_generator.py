"""随机中国大陆手机号生成。"""

from __future__ import annotations

import random

# 常见号段前缀（满足测试造数，不保证号段实时完整）
_PREFIXES = [
    "130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
    "150", "151", "152", "153", "155", "156", "157", "158", "159",
    "166", "167",
    "170", "171", "172", "173", "175", "176", "177", "178",
    "180", "181", "182", "183", "184", "185", "186", "187", "188", "189",
    "191", "198", "199",
]


def generate_phone(prefix: str | None = None) -> str:
    """生成 11 位中国大陆手机号。

    Args:
        prefix: 指定号段前缀（3 位）；默认从常见号段随机选取。

    Returns:
        如 ``13812345678``。
    """
    head = prefix or random.choice(_PREFIXES)
    if not head.isdigit() or len(head) != 3:
        raise ValueError("prefix 必须是 3 位数字")
    tail = "".join(str(random.randint(0, 9)) for _ in range(8))
    return f"{head}{tail}"
