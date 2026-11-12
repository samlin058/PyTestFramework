from __future__ import annotations

import sys

from loguru import logger

from service.utils.path_util import PROJECT_ROOT, ensure_dir

_CONFIGURED = False


def _configure() -> None:
    """配置 loguru：控制台仅 WARNING+，详细日志写入按日滚动的文件。"""
    global _CONFIGURED
    if _CONFIGURED:
        return
    log_dir = ensure_dir(PROJECT_ROOT / "logs")
    logger.remove()
    logger.add(
        sys.stderr,
        level="WARNING",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    )
    logger.add(
        log_dir / "framework_{time:YYYYMMDD}.log",
        rotation="10 MB",
        retention="14 days",
        encoding="utf-8",
        level="DEBUG",
    )
    _CONFIGURED = True


def get_logger():
    """获取已配置的全局 logger 实例。"""
    _configure()
    return logger


_configure()
