# PyTestFramework

基于 **Pytest + Requests + Playwright + Allure** 的接口 / UI 自动化测试框架。按「资产 → 业务 → 用例」分层，支持 YAML 接口契约、数据驱动、造数工厂、多环境配置与 Jenkins / Docker 持续集成。

## 特性

- **API + UI 统一工程**：同一套配置、日志、断言与报告体系
- **YAML 接口契约**：`assets/api/<项目>/*.yaml` 定义 controller / name / method / url；单接口用 `HttpClient.call`
- **业务层编排**：`business` 串联多接口与可选 DB，暴露场景方法供工厂与用例复用；断言写在 `testCases`
- **数据驱动**：支持 YAML / JSON / Excel，配合 `@pytest.mark.parametrize`
- **造数工厂**：API 造数 + 可选 MySQL DB 造数
- **Allure 报告**：请求/响应自动附件，UI 失败自动截图
- **多环境 / 多项目**：`config/{dev,test,prod}.yaml` 内按 `projects` 分项目；命令行 `ENV` 切换环境
- **CI**：Jenkinsfile 与 Docker Compose 开箱可用

## 技术栈

| 组件 | 用途 |
|------|------|
| Pytest / pytest-xdist / pytest-rerunfailures | 执行、并行、失败重跑 |
| Requests | HTTP 客户端 |
| Playwright | UI 自动化 |
| Allure | 测试报告 |
| PyYAML / openpyxl | 配置与数据驱动 |
| jsonpath-ng | JSON 断言 |
| loguru | 日志 |
| PyMySQL | 可选数据库造数 |
| python-dotenv | 环境变量 |

## 目录结构

```text
PyTestFramework/
├── assets/                     # 测试资产（不写业务逻辑）
│   ├── api/<项目>/             # 接口 YAML 契约（如 AITF/UserController.yaml）
│   └── ui/<项目>/
│           ├── elements/           # 元素定义（可扩展）
│           └── pages/              # Page Object（BasePage / LoginPage）
├── business/                   # 业务层（多接口/DB 场景编排；无断言、无单接口透传）
│   ├── api/<项目>/             # 如 user_biz.py（场景方法）
│   └── ui/<项目>/              # 如 login_biz.py
├── core/                       # 框架核心能力
│   ├── assert_utils/           # 断言工具
│   ├── config/                 # 环境配置加载
│   ├── data_driver/            # YAML/JSON/Excel 数据加载
│   ├── database/               # MySQL 客户端
│   ├── http/                   # HttpClient + ApiSpecLoader
│   ├── logger/                 # loguru 日志
│   └── utils/                  # 路径等工具
├── datafactory/                # 造数工厂
│   ├── api/<项目>/             # 接口造数
│   └── db/                     # 数据库造数
├── execution/                  # Pytest 插件层
│   ├── fixtures/               # http_client / page / db 等
│   ├── hooks/                  # 失败截图等 hook
│   └── markers.py              # 标记常量
├── testCases/                  # 用例（唯一入口）
│   ├── api/<项目>/             # API 用例 + DDT 数据
│   ├── ui/<项目>/              # UI 用例 + data 数据
│   └── conftest.py             # 注册 fixtures / hooks
├── config/                     # dev.yaml / test.yaml / prod.yaml
├── report_ci/                  # CI 通知等
├── reports/                    # Allure 结果（运行生成，已 gitignore）
├── logs/                       # 框架日志（运行生成）
├── pytest.ini
├── requirements.txt
├── Dockerfile / docker-compose.yml
└── Jenkinsfile
```

### 分层约定

| 层级 | 职责 | 示例 |
|------|------|------|
| `assets` | 接口契约、页面元素与操作 | `UserController.yaml`、`LoginPage` |
| `HttpClient.call` | 单接口调用（按 controller + name） | `http_client.call("UserController", "login", ...)` |
| `business` | 多接口串联 / 可选 DB 的场景编排（不含断言） | `UserBiz.login_and_get_user()` |
| `datafactory` | 前置造数（单接口直调或复用 business） | `UserDataFactory.create_user()` |
| `testCases` | 调 call / business + 断言 | `test_user_login.py` |
| `core` / `execution` | 框架能力，一般不改业务代码 | HttpClient、fixtures |

```text
testCases ──┬── 单接口用例 → HttpClient.call(controller, name)
            └── 场景用例   → Business.scenario(...)
datafactory ──┬── 简单造数 → HttpClient.call
              └── 复杂前置 → Business.scenario(...)
Business ─────────────────→ HttpClient.call + DatabaseClient
HttpClient ───────────────→ assets YAML
```

## 快速开始

### 1. 环境准备

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置环境

环境配置统一写在 `config/*.yaml`（如 `dev.yaml`、`test.yaml`），启动时按 `ENV` 加载对应文件。

说明：

- 默认 `ENV=test`，即加载 `config/test.yaml`
- 切换环境请在命令行指定，例如：

```bash
# PowerShell
$env:ENV="dev"; pytest

# CMD
set ENV=dev && pytest

# Linux / macOS
ENV=dev pytest
```

- 跑 UI 用例前须在对应项目下配置 `projects.<项目>.ui.base_url`，否则会抛出 `UsageError`

### 3. 运行用例

```bash
# 全部用例
pytest

# 仅 API / UI / 冒烟
pytest -m api
pytest -m ui
pytest -m smoke

# 指定文件或目录
pytest testCases/api/AITF
pytest testCases/ui/AITF/test_login_page.py

# 并行（需 pytest-xdist）
pytest -n auto -m api

# 失败重跑
pytest --reruns 1 -m api
```

### 4. 查看 Allure 报告

`pytest.ini` 已默认输出到 `reports/allure-results`：

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 配置说明

配置按「运行环境 × 项目」组织：先用 `ENV` 选择 `config/{ENV}.yaml`，再按用例路径中的项目名（如 `testCases/api/AITF/...` → `AITF`）加载 `projects.<项目>`，并与 `defaults` 深度合并。

`config/test.yaml` 示例：

```yaml
env: test
defaults:
  timeout: 10
  ui:
    headless: true
    default_timeout: 10
    navigation_timeout: 30
notify:
  webhook: ""
projects:
  AITF:
    api_base_url: https://reqres.in
    ui:
      base_url: ""
    db:
      enabled: false
      host: 127.0.0.1
      port: 3306
      user: root
      password: ""
      database: aitf
  # OtherApp:
  #   api_base_url: https://other-api.example
  #   ui:
  #     base_url: https://other-ui.example
  #   db:
  #     enabled: true
  #     host: 127.0.0.1
  #     port: 3306
  #     user: root
  #     password: ""
  #     database: other
```

| 配置项 | 说明 |
|--------|------|
| `defaults.*` | 各项目共用的默认值（超时、UI 等） |
| `projects.<项目>.api_base_url` | 该项目 API 根地址 |
| `projects.<项目>.ui.base_url` | 该项目 UI 入口地址 |
| `projects.<项目>.db` | 该项目数据库连接（按项目配置，无 defaults） |
| `projects.<项目>.timeout` / `ui` | 可覆盖 defaults 中同名项 |
| `notify.webhook` | 全局通知 webhook（钉钉 / 企微等） |

新增项目时：在 `projects` 下增加同名段，并保持目录约定 `testCases/api|<ui>/<项目>/`、`assets/.../<项目>/`。

可选环境变量：`PROJECT=AITF` 时，`API_BASE_URL` / `UI_*` / `DB_*` 只覆盖该项目；未指定 `PROJECT` 则覆盖配置中全部项目。

## 编写 API 用例

### 1. 定义接口契约

`assets/api/<项目>/UserController.yaml`：

```yaml
controller: UserController
apis:
  - name: login
    method: POST
    url: /api/login
    headers:
      Content-Type: application/json
  - name: getUser
    method: GET
    url: /api/users/{id}
```

单接口通过 `(controller, name)` 定位契约；路径参数用 `path_params` 替换 `{id}`。

### 2. 单接口调用

```python
resp = http_client.call(
    "UserController",
    "login",
    json={"email": email, "password": password},
)
```

同一 controller 下 `name` 必须唯一。需要按 url 调试时仍可用 `http_client.request(controller, url, ...)`。

### 3. 业务场景编排（非单接口透传）

`business/api/<项目>/user_biz.py` 只写多接口串联 / 可选 DB 的场景，供工厂与用例复用，**不做断言**：

```python
class UserBiz:
    CONTROLLER = "UserController"

    def login_and_get_user(self, *, email: str, password: str, user_id=2) -> dict:
        login_resp = self.client.call(
            self.CONTROLLER, "login", json={"email": email, "password": password}
        )
        get_resp = self.client.call(
            self.CONTROLLER, "getUser", path_params={"id": user_id}
        )
        return {"login_resp": login_resp, "get_resp": get_resp, "token": ..., ...}
```

### 4. 编写用例 + 数据驱动

用例文件：`testCases/api/<项目>/test_*.py`  
数据文件：放在同级 `data/` 下，`parametrize_data` 只需传文件名。

```python
# 单接口：直接 call
resp = http_client.call("UserController", "login", json={...})

# 场景：调 business
result = UserBiz(http_client).login_and_get_user(email=..., password=..., user_id=2)
AssertUtils.status_code(result["login_resp"], 200)
```

`testCases/api`、`testCases/ui` 下的用例会自动打上 `pytest.mark.api` / `pytest.mark.ui`，以及 Allure Feature `API` / `UI`，用例里不必再写。

内置 fixture：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `project_name` | function | 从用例路径解析项目名 |
| `project_config` | function | 当前项目合并后的配置 |
| `http_client` | function | 按项目缓存的 `HttpClient` |
| `env_config` | session | 当前环境完整配置 |
| `db` | function | 按项目的 `DatabaseClient`（未启用时为 no-op） |
| `user_factory` | function | `UserDataFactory` |

## 编写 UI 用例

### 1. Page Object

`assets/ui/pages/login_page.py` 继承 `BasePage`，只封装定位与基础操作。

### 2. 业务层

`business/ui/login_biz.py` 组合页面动作并返回结果，不做断言。

### 3. 用例

```python
@allure.story("Login Page")
@pytest.mark.smoke
@pytest.mark.parametrize("case", parametrize_data("login_cases.yaml"))
def test_login_page(page, ui_base_url, case):
    biz = LoginBiz(page, ui_base_url)
    msg = biz.login(case["username"], case["password"])
    AssertUtils.contains(msg, "Login success")
```

内置 UI fixture：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `ui_base_url` | function | 当前项目的 UI 地址 |
| `browser` | session | Chromium 浏览器（headless 取 defaults） |
| `page` | function | 独立 context + page；超时取当前项目 UI 配置 |

失败时 `execution/hooks/pytest_hooks.py` 会自动截图并附加到 Allure。

## 数据驱动

`core.data_driver.parametrize_data` 支持：

- `.yaml` / `.yml`：默认取文档中的 `cases` 列表
- `.json`：同上
- `.xlsx` / `.xls`：首行为表头，返回 `list[dict]`

路径约定：只传文件名时，自动加载**调用方用例同级** `data/<文件名>`（如 `testCases/api/AITF/data/login_cases.yaml`）。仍兼容绝对路径，以及相对项目根 / `testCases/` 的路径。

## 造数工厂

```python
# 简单 API 造数（单接口 HttpClient.call）
user = user_factory.create_user(name="factory_user", job="qa")

# 复杂前置（复用 business 场景）
ctx = user_factory.login_and_get_user(user_id=2)

# DB 造数（需 projects.<项目>.db.enabled=true，并配置连接信息）
user_factory.insert_user_row(name="db_user", email="a@b.com")
```

简单造数可直调单接口；复杂前置优先走 `business` 场景方法。

## 断言与日志

```python
from core.assert_utils import AssertUtils
from core.logger import logger

AssertUtils.status_code(resp, 200)
AssertUtils.equal(actual, expected)
AssertUtils.contains(body, "token")
AssertUtils.json_path_equals(body, "$.data.id", 1)
AssertUtils.true(condition, "说明")

logger.info("自定义日志")
```

日志输出到控制台与 `logs/framework_YYYYMMDD.log`。

## Pytest 标记

在 `pytest.ini` 中声明：

| 标记 | 含义 |
|------|------|
| `smoke` | 冒烟 |
| `api` | 接口用例 |
| `ui` | UI 用例 |
| `regression` | 回归 |

常量见 `execution/markers.py`。

## Docker

```bash
# 默认跑 API 用例，结果挂载到 ./reports
docker compose up --build
```

或：

```bash
docker build -t pytest-framework .
docker run --rm -e ENV=test -v %CD%/reports:/app/reports pytest-framework
```

## Jenkins

`Jenkinsfile` 流水线阶段：

1. Checkout
2. Setup（venv + 依赖 + Playwright Chromium）
3. Test（`pytest -m "api or ui"`）
4. Allure Report
5. Notify（`report_ci.notify.webhook.send_webhook`）
6. 归档 `reports/**`

配置 Jenkins 凭据 / 环境变量后，将 `NOTIFY_WEBHOOK`、`UI_BASE_URL` 等注入即可。

> `.gitlab-ci.yml` 仅为占位，当前以 Jenkins 为主。

## 扩展新项目（建议步骤）

以新增项目 `FOO` 为例：

1. `assets/api/FOO/*.yaml` — 写接口契约（含唯一 `name`）  
2. 单接口用例 / 简单造数 — `HttpClient.call(controller, name, ...)`
3. `business/api/FOO/*_biz.py` — 只写需要串联的场景方法
4. `datafactory/api/FOO/*_factory.py` — 按需造数（可复用 business）
5. `testCases/api/FOO/test_*.py` + `data/*.yaml` — 写用例与数据
6. UI 同理：`assets/ui/pages` → `business/ui` → `testCases/ui/FOO`

保持用例薄、场景可复用、契约与编排分离，便于多项目并行维护。

## 示例工程说明

仓库内置 **AITF** 示例，对接 [ReqRes](https://reqres.in) 演示 API 登录 / 造数；UI 登录页为 Page Object 模板，需自行配置真实 `UI_BASE_URL` 后验证。

## License

Internal use / 按团队约定。
