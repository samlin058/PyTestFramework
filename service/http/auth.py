from __future__ import annotations


def authorization_value(token: str) -> str:
    """将登录返回的 token 转为 Authorization 头值（DRF TokenAuthentication）。"""
    value = token.strip()
    if value.lower().startswith(("token ", "bearer ")):
        return value
    return f"Token {value}"
