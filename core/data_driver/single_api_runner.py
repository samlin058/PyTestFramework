from __future__ import annotations

from typing import Any

import allure

from core.config import get_project_config
from core.data_driver.single_api_asserter import extract_vars, run_assertions
from core.data_driver.single_api_placeholder import bind_factory_context, resolve_placeholders
from core.database import DatabaseClient
from core.http import HttpClient
from core.logger import logger


def run_single_api_case(
    unit: dict[str, Any],
    *,
    http_client: HttpClient | None = None,
    db: DatabaseClient | None = None,
) -> Any:
    """执行单条单接口 YAML case：占位符 → HTTP → extract → assertions。"""
    project = unit["project"]
    controller = unit["controller"]
    api_name = unit["api_name"]
    case = unit["case"]
    request_data = dict(unit["request"])

    project_config = get_project_config(project)
    global_var = dict(project_config.get("global_var") or {})

    client = http_client or HttpClient(project=project)
    factory_context = bind_factory_context(http_client=client, db=db)

    case_id = case.get("case_id") or f"case_{unit.get('case_index', 0)}"
    case_name = case.get("name") or case_id
    module = unit.get("module") or project
    api_desc = unit.get("api_desc") or f"{controller}.{api_name}"

    allure.dynamic.feature(str(module))
    allure.dynamic.story(str(api_desc))
    allure.dynamic.title(f"{case_id} - {case_name}")

    with allure.step("resolve placeholders"):
        resolved = resolve_placeholders(
            request_data,
            global_var=global_var,
            factory_context=factory_context,
        )

    headers = resolved.get("headers")
    params = resolved.get("params")
    path_params = resolved.get("path_params")
    body = resolved.get("body")

    logger.info(
        f"Single API case {case_id}: {controller}.{api_name} project={project}"
    )
    response = client.call(
        controller,
        api_name,
        headers=headers,
        params=params,
        path_params=path_params,
        json=body,
    )

    try:
        payload = response.json()
    except Exception:
        payload = None

    variables = extract_vars(payload, case.get("extract"))
    run_assertions(
        response=response,
        assertions=case.get("assertions"),
        db=db,
        variables=variables,
    )
    return response
