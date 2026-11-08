"""随机时间戳生成。"""

from __future__ import annotations

import random
import time
from datetime import date, datetime


def generate_timestamp(
    start: str | date | datetime | int | float | None = None,
    end: str | date | datetime | int | float | None = None,
    *,
    unit: str = "s",
    as_string: bool = False,
) -> int | str:
    """在指定区间内随机生成一个时间戳。

    Args:
        start: 起始时间；支持时间戳、``YYYY-MM-DD``、date、datetime；默认 1970-01-01。
        end: 结束时间；同上，默认当前时间。
        unit: ``s`` 秒级，``ms`` 毫秒级。
        as_string: True 返回字符串，False 返回整数。

    Returns:
        随机时间戳（秒或毫秒）。
    """
    if unit not in {"s", "ms"}:
        raise ValueError("unit 仅支持 's' 或 'ms'")

    start_ts = _to_seconds(start) if start is not None else 0.0
    end_ts = _to_seconds(end) if end is not None else time.time()

    if start_ts > end_ts:
        raise ValueError(f"start ({start_ts}) 不能晚于 end ({end_ts})")

    value = random.uniform(start_ts, end_ts)
    result = int(value * 1000) if unit == "ms" else int(value)
    return str(result) if as_string else result


def _to_seconds(value: str | date | datetime | int | float) -> float:
    if isinstance(value, (int, float)):
        # 13 位按毫秒处理，其余按秒处理
        return float(value) / 1000.0 if value > 1e12 else float(value)
    if isinstance(value, datetime):
        return value.timestamp()
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time()).timestamp()
    return datetime.strptime(value, "%Y-%m-%d").timestamp()
