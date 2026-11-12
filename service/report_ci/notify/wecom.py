from __future__ import annotations

from typing import Any


def build_text_payload(content: str) -> dict[str, Any]:
    return {"msgtype": "text", "text": {"content": content}}


def build_markdown_payload(content: str) -> dict[str, Any]:
    return {"msgtype": "markdown", "markdown": {"content": content}}


def build_mention_text_payload(content: str, *, mention_all: bool = False) -> dict[str, Any]:
    payload = build_text_payload(content)
    if mention_all:
        payload["text"]["mentioned_list"] = ["@all"]
    return payload
