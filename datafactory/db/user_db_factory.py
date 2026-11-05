from __future__ import annotations

from typing import Any

import allure

from core.database import DatabaseClient
from core.logger import logger


class UserDbFactory:
    def __init__(self, db: DatabaseClient) -> None:
        self.db = db

    @allure.step("DB造数: 插入用户")
    def insert_user(self, name: str, email: str) -> dict[str, Any]:
        self.db.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email),
        )
        row = self.db.fetch_one("SELECT * FROM users WHERE email=%s ORDER BY id DESC LIMIT 1", (email,))
        logger.info(f"Inserted user via DB: {row}")
        return row or {"name": name, "email": email}

    @allure.step("DB造数: 按邮箱删除用户")
    def delete_user_by_email(self, email: str) -> int:
        return self.db.execute("DELETE FROM users WHERE email=%s", (email,))
