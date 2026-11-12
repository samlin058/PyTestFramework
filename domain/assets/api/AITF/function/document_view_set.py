from __future__ import annotations

from typing import Any

import allure

from service.http import ApiResponse, HttpClient, authorization_value


class DocumentViewSet:
    """DocumentViewSet 单接口调用封装（由 api_info/DocumentViewSet.yaml 生成）。"""

    def __init__(self, http_client: HttpClient | None = None) -> None:
        self.client = http_client or HttpClient(project="AITF")


    @allure.step("接口请求: DocumentViewSet.list")
    def list(
        self,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.list — GET /api/documents/。"""
        method = "GET"
        url = "/api/documents/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.list",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.create")
    def create(
        self,
        *,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.create — POST /api/documents/。"""
        method = "POST"
        url = "/api/documents/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = None
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.create",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.retrieve")
    def retrieve(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.retrieve — GET /api/documents/{id}/。"""
        method = "GET"
        url = "/api/documents/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.retrieve",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.update")
    def update(
        self,
        *,
        id_: int | str,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.update — PUT /api/documents/{id}/。"""
        method = "PUT"
        url = "/api/documents/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.update",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.partial_update")
    def partial_update(
        self,
        *,
        id_: int | str,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.partial_update — PATCH /api/documents/{id}/。"""
        method = "PATCH"
        url = "/api/documents/{id}/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.partial_update",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.destroy")
    def destroy(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.destroy — DELETE /api/documents/{id}/。"""
        method = "DELETE"
        url = "/api/documents/{id}/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.destroy",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.get_content")
    def get_content(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.get_content — GET /api/documents/{id}/content/。"""
        method = "GET"
        url = "/api/documents/{id}/content/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.get_content",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.update_content")
    def update_content(
        self,
        *,
        id_: int | str,
        content: str | None = None,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.update_content — PUT /api/documents/{id}/content/。"""
        method = "PUT"
        url = "/api/documents/{id}/content/"
        default_headers = {"Content-Type": "application/json"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        if json is not None:
            payload = json
        else:
            payload = {}
            if content is not None:
                payload["content"] = content
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.update_content",
            json=payload,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.download")
    def download(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.download — GET /api/documents/{id}/download/。"""
        method = "GET"
        url = "/api/documents/{id}/download/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.download",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.preview")
    def preview(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.preview — GET /api/documents/{id}/preview/。"""
        method = "GET"
        url = "/api/documents/{id}/preview/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.preview",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.render_status")
    def render_status(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.render_status — GET /api/documents/{id}/render-status/。"""
        method = "GET"
        url = "/api/documents/{id}/render-status/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.render_status",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.render_preview")
    def render_preview(
        self,
        *,
        id_: int | str,
        json: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.render_preview — POST /api/documents/{id}/render-preview/。"""
        method = "POST"
        url = "/api/documents/{id}/render-preview/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.render_preview",
            json=json,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.upload")
    def upload(
        self,
        *,
        id_: int | str,
        file: Any,
        data: Any = None,
        files: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.upload — POST /api/documents/{id}/upload/。"""
        method = "POST"
        url = "/api/documents/{id}/upload/"
        default_headers = {"Content-Type": "multipart/form-data"}
        merged_headers = {**default_headers, **(headers or {})}
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        resolved_files = files
        if resolved_files is None:
            resolved_files = {"file": file}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.upload",
            files=resolved_files,
            data=data,
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.revisions")
    def revisions(
        self,
        *,
        id_: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.revisions — GET /api/documents/{id}/revisions/。"""
        method = "GET"
        url = "/api/documents/{id}/revisions/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.revisions",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.revision_content")
    def revision_content(
        self,
        *,
        id_: int | str,
        revision_no: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.revision_content — GET /api/documents/{id}/revisions/{revision_no}/content/。"""
        method = "GET"
        url = "/api/documents/{id}/revisions/{revision_no}/content/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_, "revision_no": revision_no}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.revision_content",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )


    @allure.step("接口请求: DocumentViewSet.revision_download")
    def revision_download(
        self,
        *,
        id_: int | str,
        revision_no: int | str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """调用 DocumentViewSet.revision_download — GET /api/documents/{id}/revisions/{revision_no}/download/。"""
        method = "GET"
        url = "/api/documents/{id}/revisions/{revision_no}/download/"
        merged_headers = dict(headers or {})
        if token:
            merged_headers["Authorization"] = authorization_value(token)
        path_params = {"id": id_, "revision_no": revision_no}
        return self.client.send(
            method,
            url,
            name="DocumentViewSet.revision_download",
            path_params=path_params,
            params=params,
            headers=merged_headers,
            **kwargs,
        )
