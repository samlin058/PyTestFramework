from __future__ import annotations

from playwright.sync_api import Page

from core.config import get_project_config
from core.ui.page import UiPage
from core.ui.session import UiSession


class UiBizBase:
    """UI 业务基类：可注入 pytest page，或独立自启 UiSession（固定有头）。

    自启时由本类持有会话，调用 ``close()`` 关闭；注入 page 时 ``close()`` 为空操作。
    """

    def __init__(
        self,
        page: Page | None = None,
        *,
        project: str,
        elements: str,
    ) -> None:
        self.project = project
        self._session: UiSession | None = None

        cfg = get_project_config(project)
        ui_cfg = cfg.get("ui") or {}
        self.base_url = (ui_cfg.get("base_url") or "").strip().rstrip("/")

        if page is not None:
            pw_page = page
        else:
            self._session = UiSession(project)
            pw_page = self._session.start()

        self.ui = UiPage(pw_page, project=project, elements=elements)

    def close(self) -> None:
        """关闭本对象自启的浏览器会话（幂等）；pytest 注入的 page 不处理。"""
        if self._session is not None:
            self._session.close()
            self._session = None
