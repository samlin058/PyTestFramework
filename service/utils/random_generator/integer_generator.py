"""随机整数生成。"""

from __future__ import annotations

import random


def generate_integer(
    min_value: int = 0,
    max_value: int = 100,
    *,
    exclude: set[int] | list[int] | tuple[int, ...] | None = None,
) -> int:
    """在闭区间 ``[min_value, max_value]`` 内随机生成整数。

    Args:
        min_value: 最小值（含）。
        max_value: 最大值（含）。
        exclude: 需要排除的数值集合。

    Returns:
        随机整数。
    """
    if min_value > max_value:
        raise ValueError(f"min_value ({min_value}) 不能大于 max_value ({max_value})")

    blocked = set(exclude or ())
    span = max_value - min_value + 1
    if not blocked:
        return random.randint(min_value, max_value)

    if span - len(blocked) <= 0:
        raise ValueError("排除后没有可选整数")

    # 小区间直接枚举；大区间用重试，避免构造巨大列表
    if span <= 10_000:
        candidates = [n for n in range(min_value, max_value + 1) if n not in blocked]
        if not candidates:
            raise ValueError("排除后没有可选整数")
        return random.choice(candidates)

    for _ in range(1000):
        value = random.randint(min_value, max_value)
        if value not in blocked:
            return value
    raise ValueError("多次尝试后仍命中排除集合，请缩小 exclude 或区间")
