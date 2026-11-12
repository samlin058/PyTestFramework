from __future__ import annotations

import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any


def sign_webhook(webhook: str, secret: str) -> str:
    """Append DingTalk robot timestamp + sign query params when secret is configured."""
    if not secret:
        return webhook
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}"
    digest = hmac.new(
        secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(digest))
    sep = "&" if "?" in webhook else "?"
    return f"{webhook}{sep}timestamp={timestamp}&sign={sign}"


def build_text_payload(content: str, *, mention_all: bool = False) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "msgtype": "text",
        "text": {"content": content},
    }
    if mention_all:
        payload["at"] = {"isAtAll": True}
    return payload


def build_markdown_payload(
    title: str,
    content: str,
    *,
    mention_all: bool = False,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "msgtype": "markdown",
        "markdown": {"title": title, "text": content},
    }
    if mention_all:
        payload["at"] = {"isAtAll": True}
    return payload
