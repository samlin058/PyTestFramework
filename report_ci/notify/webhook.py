from __future__ import annotations

import json
from typing import Any
from urllib import request

from core.config import get_config
from core.logger import logger


def send_webhook(title: str, content: str, webhook: str | None = None) -> bool:
    """Send a simple JSON webhook notification (DingTalk/WeCom compatible skeleton)."""
    cfg = get_config().get("notify") or {}
    url = webhook or cfg.get("webhook") or ""
    if not url:
        logger.warning("Notify webhook is empty; skip notification")
        return False

    payload: dict[str, Any] = {
        "msgtype": "text",
        "text": {"content": f"{title}\n{content}"},
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=10) as resp:
            logger.info(f"Notify webhook status={resp.status}")
            return 200 <= resp.status < 300
    except Exception as exc:
        logger.error(f"Notify webhook failed: {exc}")
        return False
