"""随机字符串生成。"""

from __future__ import annotations

import random
import string

_CHARSETS = {
    "digit": string.digits,
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "letter": string.ascii_letters,
    "alnum": string.ascii_letters + string.digits,
    "hex": string.hexdigits.lower(),
    "all": string.ascii_letters + string.digits + string.punctuation,
}


def generate_string(
    length: int = 8,
    charset: str = "alnum",
    *,
    prefix: str = "",
    suffix: str = "",
    custom_chars: str | None = None,
) -> str:
    """随机生成字符串。

    Args:
        length: 随机部分长度（不含 prefix/suffix）。
        charset: 字符集名称，可选 digit / lower / upper / letter / alnum / hex / all。
        prefix: 前缀。
        suffix: 后缀。
        custom_chars: 自定义字符集；传入后忽略 ``charset``。

    Returns:
        如 ``user_aB3k9Qx2``。
    """
    if length < 0:
        raise ValueError("length 不能为负数")

    if custom_chars is not None:
        pool = custom_chars
    elif charset in _CHARSETS:
        pool = _CHARSETS[charset]
    else:
        raise ValueError(
            f"未知 charset: {charset}，可选: {', '.join(sorted(_CHARSETS))}"
        )
    if not pool:
        raise ValueError("字符集不能为空")

    body = "".join(random.choices(pool, k=length))
    return f"{prefix}{body}{suffix}"
