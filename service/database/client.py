from __future__ import annotations

from typing import Any

from service.logger import logger


class DatabaseClient:
    """Lightweight MySQL client for DataFactory. No-op when db.enabled is false."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """初始化数据库客户端，读取项目级配置并判断是否启用连接。"""
        cfg = config or {}
        self.enabled = bool(cfg.get("enabled", False))
        self.config = cfg
        self._conn = None

    def connect(self) -> None:
        """建立 MySQL 连接；若配置未启用数据库则跳过。"""
        if not self.enabled:
            logger.warning("Database is disabled in config; skip connect")
            return
        import pymysql

        self._conn = pymysql.connect(
            host=self.config.get("host", "127.0.0.1"),
            port=int(self.config.get("port", 3306)),
            user=self.config.get("user", "root"),
            password=self.config.get("password", ""),
            database=self.config.get("database", ""),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        logger.info("Database connected")

    def close(self) -> None:
        """关闭当前数据库连接并清空连接引用。"""
        if self._conn:
            self._conn.close()
            self._conn = None

    def execute(self, sql: str, args: tuple[Any, ...] | None = None) -> int:
        """执行写操作 SQL，返回受影响的行数。"""
        self._ensure_conn()
        with self._conn.cursor() as cursor:
            affected = cursor.execute(sql, args)
            return affected

    def fetch_one(self, sql: str, args: tuple[Any, ...] | None = None) -> dict[str, Any] | None:
        """执行查询并返回第一条记录（字典），无结果时返回 None。"""
        self._ensure_conn()
        with self._conn.cursor() as cursor:
            cursor.execute(sql, args)
            return cursor.fetchone()

    def fetch_all(self, sql: str, args: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        """执行查询并返回全部记录列表。"""
        self._ensure_conn()
        with self._conn.cursor() as cursor:
            cursor.execute(sql, args)
            return list(cursor.fetchall())

    def _ensure_conn(self) -> None:
        """确保数据库已启用且连接可用，必要时自动 connect。"""
        if not self.enabled:
            raise RuntimeError(
                "Database is disabled. Set projects.<project>.db.enabled=true to use DB factory."
            )
        if self._conn is None:
            self.connect()
