"""随机邮箱生成。"""

from __future__ import annotations

import random
import string
import time

_DOMAINS = [
    "qq.com",
    "foxmail.com",
    "163.com",
    "sina.com",
    "189.cn"
]


def generate_email(
    *,
    prefix: str | None = None,
    domain: str | None = None,
    length: int = 8,
) -> str:
    """生成随机邮箱地址。

    Args:
        prefix: 指定本地部分前缀；默认 ``user`` + 时间戳后 6 位，降低重复概率。
        domain: 邮箱域名；默认从常见测试域名中随机选取。
        length: 随机后缀长度（仅在未指定 ``prefix`` 时生效于随机段）。

    Returns:
        如 ``user123456ab@example.com``。
    """
    if length < 0:
        raise ValueError("length 不能为负数")

    host = domain or random.choice(_DOMAINS)
    if not host or "@" in host or " " in host:
        raise ValueError("domain 不能为空，且不能包含 @ 或空格")

    if prefix is not None:
        local = prefix
    else:
        stamp = str(int(time.time()))[-6:]
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
        local = f"user{stamp}{suffix}"

    if not local or "@" in local or " " in local:
        raise ValueError("prefix 不能为空，且不能包含 @ 或空格")

    return f"{local}@{host}"
