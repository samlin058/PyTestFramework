from __future__ import annotations

from typing import Any

from domain.assets.api.AITF.function import LoginView, UserViewSet
from service.utils.random_generator import *

# 创建新用户
def create_user(account: str, username: str, email: str, password: str) -> dict[str, Any]:
    token = LoginView().post(account="admin", password="123456")["token"]
    return UserViewSet().create(token=token, account=account, username=username, email=email, password=password)


if __name__ == "__main__":
    # 独立调试：python -m domain.business.api.AITF.user_biz
    response = create_user(
        account=generate_string(prefix="user_"),
        username=generate_chinese_name(),
        email=generate_email(),
        password="123456",
    )
    print(f"status={response.status_code}, body={response.body}")
    