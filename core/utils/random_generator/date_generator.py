"""随机日期生成。"""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta


def generate_date(
    start: str | date | datetime | None = None,
    end: str | date | datetime | None = None,
    fmt: str = "%Y-%m-%d",
    as_string: bool = True,
) -> str | date:
    """在指定区间内随机生成一个日期。

    Args:
        start: 起始日期，支持 ``YYYY-MM-DD`` / date / datetime；默认 1970-01-01。
        end: 结束日期，支持 ``YYYY-MM-DD`` / date / datetime；默认今天。
        fmt: 返回字符串时的格式，默认 ``%Y-%m-%d``。
        as_string: True 返回格式化字符串，False 返回 ``date`` 对象。

    Returns:
        随机日期字符串或 ``date`` 对象。
    """
    start_date = _to_date(start) if start is not None else date(1970, 1, 1)
    end_date = _to_date(end) if end is not None else date.today()

    if start_date > end_date:
        raise ValueError(f"start ({start_date}) 不能晚于 end ({end_date})")

    delta_days = (end_date - start_date).days
    result = start_date + timedelta(days=random.randint(0, delta_days))
    return result.strftime(fmt) if as_string else result


def generate_today(
    fmt: str = "%Y-%m-%d",
    as_string: bool = True,
) -> str | date:
    """生成当天日期。

    Args:
        fmt: 返回字符串时的格式，默认 ``%Y-%m-%d``。
        as_string: True 返回格式化字符串，False 返回 ``date`` 对象。

    Returns:
        当天日期字符串或 ``date`` 对象。
    """
    today = date.today()
    return today.strftime(fmt) if as_string else today


def _to_date(value: str | date | datetime) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()
