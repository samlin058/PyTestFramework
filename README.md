# PyTestFramework

基于 **Pytest + Requests + Playwright + Allure** 的接口 / UI 自动化测试框架。按「资产 → 业务 → 用例」分层，支持 YAML 接口契约、单接口 YAML 用例、数据驱动、造数工厂、多环境配置与 Jenkins / Docker 持续集成。

## 特性

- **API + UI 统一工程**：同一套配置、日志、断言与报告体系
- **YAML 接口契约**：`assets/api/<项目>/*.yaml` 定义 controller / name / method / url；单接口用 `HttpClient.call`
- **单接口 YAML 用例**：`testCases/api/<项目>/single/*.yaml` 由插件自动收集，无需写 `test_*.py`
- **业务层编排**：`business` 串联多接口与可选 DB，暴露场景方法供工厂与用例复用；断言写在 `testCases`
- **数据驱动**：支持 YAML / JSON / Excel，配合 `@pytest.mark.parametrize`
- **造数工厂**：API 造数 + 可选 MySQL DB 造数；单接口 YAML 可用占位符调用工厂
- **Allure 报告**：请求/响应自动附件，UI 失败自动截图
- **多环境 / 多项目**：`config/{dev,test,prod}.yaml` 内按 `projects` 分项目；命令行 `ENV` 切换环境
- **CI**：Jenkinsfile 与 Docker Compose 开箱可用（Docker 默认只跑 API）

## 技术栈

| 组件 | 用途 |
|------|------|
| Pytest / pytest-xdist / pytest-rerunfailures | 执行、并行、失败重跑 |
| Requests | HTTP 客户端 |
| Playwright | UI 自动化 |
| Allure | 测试报告 |
| PyYAML / openpyxl | 配置与数据驱动 |
| jsonpath-ng | JSON 断言 / 提取 |
| loguru | 日志 |
| PyMySQL | 可选数据库造数 |
| python-dotenv | 环境变量（可选） |

## 目录结构

```text
PyTestFramework/
├── assets/                     # 测试资产（不写业务逻辑）
│   ├── api/<项目>/             # 接口 YAML 契约（如 AITF/LoginView.yaml）
│   └── ui/<项目>/              # 页面元素定位 YAML（按页面命名，如 login.yaml）
├── business/                   # 业务层（多接口/DB 场景编排；无断言、无单接口透传）
│   ├── api/<项目>/             # 如 user_biz.py（场景方法）
│   └── ui/<项目>/              # 如 login_biz.py（页面操作流程）
├── core/                       # 框架核心能力
│   ├── assert_utils/           # 断言工具
│   ├── config/                 # 环境配置加载
│   ├── data_driver/            # DDT 加载 + 单接口 YAML 插件/占位符/断言
│   ├── database/               # MySQL 客户端
│   ├── http/                   # HttpClient + ApiSpecLoader
│   ├── ui/                     # UiSession / UiPage / elements_loader
│   ├── logger/                 # loguru 日志
│   └── utils/                  # 路径工具、random_generator 等
├── datafactory/                # 造数工厂
│   ├── api/<项目>/             # 接口造数
│   └── db/<项目>/              # 数据库造数
├── execution/                  # Pytest 插件层
│   ├── fixtures/               # http_client / page / db 等
│   ├── hooks/                  # 失败截图、按 -m 跳过目录等
│   └── markers.py              # 标记常量
├── testCases/                  # 用例（唯一入口）
│   ├── api/<项目>/
│   │   ├── single/             # 单接口 YAML 用例（插件收集）
│   │   └── scenario/           # Python 场景用例 + data/
│   ├── ui/<项目>/              # UI 用例 + data/
│   └── conftest.py             # 注册 fixtures / hooks / single_api_plugin
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
| `assets` | 接口契约、页面元素定位 | `LoginView.yaml`、`ui/AITF/login.yaml` |
| `HttpClient.call` | 单接口调用（按 controller + name） | `http_client.call("LoginView", "post", ...)` |
| `testCases/.../single` | 单接口 YAML 用例（插件执行 + 断言） | `single/user_login.yaml` |
| `business` | 多接口串联 / 可选 DB 的场景编排（不含断言） | `UserBiz.login_and_get_user()` |
| `datafactory` | 前置造数（单接口直调或复用 business） | `UserDataFactory.create_user()` |
| `testCases/.../scenario` / `ui` | 调 call / business + 断言 | `scenario/test_user_login.py` |
| `core` / `execution` | 框架能力，一般不改业务代码 | HttpClient、fixtures、single_api_plugin |

```text
testCases ──┬── single/*.yaml  → single_api_plugin → HttpClient.call + YAML 断言
            ├── scenario/*.py  → HttpClient.call / Business.scenario(...)
            └── ui/*.py        → Business UI + 断言
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

本地若已有 `venv/`，激活对应目录即可。

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

# 仅 API / UI / 冒烟（hooks 会按 -m 跳过另一侧目录）
pytest -m api
pytest -m ui
pytest -m smoke

# 指定文件或目录
pytest testCases/api/AITF
pytest testCases/api/AITF/single
pytest testCases/api/AITF/scenario
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
    headless: false             # pytest fixture 浏览器有头/无头
    default_timeout: 10
    navigation_timeout: 30
notify:
  webhook: ""
projects:
  AITF:
    api_base_url: http://127.0.0.1:8000/
    ui:
      base_url: http://127.0.0.1:5173/
    db:
      enabled: false
      host: 127.0.0.1
      port: 3306
      user: root
      password: ""
      database: aitf
    global_var:                 # 单接口 YAML 可用 #{user} 引用
      user: admin
      password: 123456
# OtherApp:
#   api_base_url: https://other-api.example
#   ui:
#     base_url: https://other-ui.example
#   db:
#     enabled: true
#     ...
```

| 配置项 | 说明 |
|--------|------|
| `defaults.*` | 各项目共用的默认值（超时、UI 等） |
| `defaults.ui.headless` | pytest / testCases 浏览器有头/无头 |
| `projects.<项目>.api_base_url` | 该项目 API 根地址 |
| `projects.<项目>.ui.base_url` | 该项目 UI 入口地址 |
| `projects.<项目>.db` | 该项目数据库连接（按项目配置，无 defaults） |
| `projects.<项目>.global_var` | 项目级变量（单接口 YAML `#{}` 占位符） |
| `projects.<项目>.timeout` / `ui` | 可覆盖 defaults 中同名项 |
| `notify.webhook` | 全局通知 webhook（钉钉 / 企微等） |

新增项目时：在 `projects` 下增加同名段，并保持目录约定 `testCases/api|<ui>/<项目>/`、`assets/.../<项目>/`、`business/api|<ui>/<项目>/`。

可选环境变量：

- `NOTIFY_WEBHOOK` → 覆盖 `notify.webhook`
- `UI_HEADLESS` → 覆盖 `defaults.ui.headless`（`1` / `true` / `yes`）
- `PROJECT=AITF` 时，下列变量只覆盖该项目；未指定 `PROJECT` 则覆盖配置中全部项目：
  - `API_BASE_URL` → `api_base_url`
  - `UI_BASE_URL` → `ui.base_url`
  - `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` → `db.*`

## 编写 API 用例

API 用例分两类，目录分开：

| 类型 | 目录 | 写法 |
|------|------|------|
| 单接口 | `testCases/api/<项目>/single/*.yaml` | 插件自动收集，YAML 内写请求覆盖与断言 |
| 场景 | `testCases/api/<项目>/scenario/test_*.py` | Python 调 `HttpClient.call` / `business`，断言写在用例里 |

### 1. 定义接口契约

`assets/api/<项目>/LoginView.yaml`：

```yaml
controller: LoginView
apis:
  - name: post
    method: POST
    url: /api/auth/login/
    headers:
      Content-Type: application/json
    body:                    # 可选：默认 body / 字段说明
      type: object
      properties:
        account:
          type: string
          default: admin
        password:
          type: string
          default: 123456
```

单接口通过 `(controller, name)` 定位契约；路径参数用 `path_params` 替换 `{id}`。同一 controller 下 `name` 必须唯一。

### 2. 单接口 YAML 用例（推荐日常接口回归）

放到 `testCases/api/<项目>/single/`，由 `core.data_driver.single_api_plugin`（在 `testCases/conftest.py` 注册）自动收集，无需 `test_*.py`。

```yaml
module: AITF用户接口
api_desc: 用户登录
controller: LoginView
api_name: post
cases:
  - case_id: API-LOGIN-001
    name: 使用 assets 默认 body 登录成功
    assertions:
      - type: status_code
        expected: 200

  - case_id: API-LOGIN-002
    name: 显式 body 登录
    body:
      account: "#{user}"
      password: "#{password}"
    assertions:
      - type: status_code
        expected: 200
      - type: json_path
        path: "$.token"
        operator: exists
```

要点：

- 必填：`controller`、`api_name`、非空 `cases[]`
- case 可覆盖 `headers` / `params` / `body` / `path_params`，并与 assets 默认值合并
- 断言类型：`status_code` | `json_path` | `db`
- 可用 `extract` 从响应 JSONPath 提取变量，供后续断言（如 DB SQL 中的 `{{var}}`）

占位符（在 body / headers 等字符串中）：

| 语法 | 含义 |
|------|------|
| `#{key}` | `projects.<项目>.global_var` |
| `${module.func}` | `core.utils.random_generator` 下的生成器 |
| `@{api....}` / `@{db....}` | 调用 `datafactory` 造数方法 |

### 3. 单接口 Python 调用

场景用例或工厂里仍可直接：

```python
resp = http_client.call(
    "LoginView",
    "post",
    json={"account": account, "password": password},
)
```

需要按 url 调试时仍可用 `http_client.request(controller, url, ...)`。

### 4. 业务场景编排（非单接口透传）

`business/api/<项目>/*_biz.py` 只写多接口串联 / 可选 DB 的场景，供工厂与用例复用，**不做断言**。`controller` / `name` 必须与 `assets` 中契约一致。

```python
class UserBiz:
    CONTROLLER = "LoginView"  # 示例：与 assets 对齐

    def login_and_get_user(self, *, account: str, password: str, user_id=2) -> dict:
        login_resp = self.client.call(
            self.CONTROLLER, "post", json={"account": account, "password": password}
        )
        # ... 再 call 其它接口，组装上下文返回
        return {"login_resp": login_resp, "token": ..., ...}
```

### 5. 场景用例 + 数据驱动

用例文件：`testCases/api/<项目>/scenario/test_*.py`  
数据文件：放在同级 `data/` 下（如 `scenario/data/login_cases.yaml`），`parametrize_data` 只需传文件名。

```python
# 单接口：直接 call
resp = http_client.call("LoginView", "post", json={...})

# 场景：调 business
result = UserBiz(http_client).login_and_get_user(...)
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
| `user_factory` | function | `UserDataFactory`（AITF 示例） |

## 编写 UI 用例

### 1. 元素定位

`assets/ui/<项目>/<页面>.yaml`：只存 selector（扫描落盘也写这里）。支持扁平键，或包在 `elements:` 下。

```yaml
account: "#account"
password: "#password"
show_password: "[aria-label='Show']"
submit: "button[type='submit']"
message: ".ant-message"
```

通用操作在 `core.ui.UiPage`（`open` / `type` / `click` / `text_of` / `locator`）。

### 2. 业务层

`business/ui/<项目>/login_biz.py` 用 `UiPage` 封装页面操作流程，不做断言。支持双模式：

- **pytest 注入**：`LoginBiz(page)`，有头/无头由 `defaults.ui.headless` 决定
- **独立运行**：`LoginBiz(project="AITF")`，自启 `UiSession`（固定有头）

```python
from business.ui.AITF.login_biz import LoginBiz

# 不经 pytest（调试）
biz = LoginBiz(project="AITF")
biz.login("admin", "123456")
```

### 3. 用例

`testCases/ui/conftest.py` 会自动：打 `ui` 标记、Allure Feature=`UI`，并在每条用例前 `page.goto(ui_base_url)`。

```python
from business.ui.AITF.login_biz import LoginBiz

@allure.story("Login Page")
@pytest.mark.smoke
@pytest.mark.parametrize("case", parametrize_data("login_cases.yaml"))
def test_login_page(page, case):
    biz = LoginBiz(page)
    msg = biz.login(case["username"], case["password"])
    AssertUtils.contains(msg, "Login success")
```

数据文件放在用例同级 `data/`（如 `testCases/ui/AITF/data/login_cases.yaml`）。

内置 UI fixture：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `ui_base_url` | function | 当前项目的 UI 地址（未配置则报错） |
| `playwright_instance` | session | Playwright 实例 |
| `browser` | session | Chromium（`defaults.ui.headless`，最大化窗口） |
| `page` | function | 独立 context + page；超时取当前项目 UI 配置 |

失败时 `execution/hooks/pytest_hooks.py` 会自动截图并附加到 Allure（带 `api` 标记或无 `page` 时跳过）。

## 数据驱动

`core.data_driver.parametrize_data` 支持：

- `.yaml` / `.yml`：默认取文档中的 `cases` 列表
- `.json`：同上
- `.xlsx` / `.xls`：首行为表头，返回 `list[dict]`

路径约定：只传文件名时，自动加载**调用方用例同级** `data/<文件名>`（如 `testCases/api/AITF/scenario/data/login_cases.yaml`、`testCases/ui/AITF/data/login_cases.yaml`）。仍兼容绝对路径，以及相对项目根 / `testCases/` 的路径。

## 造数工厂

```python
# 简单 API 造数（单接口 HttpClient.call）
user = user_factory.create_user(name="factory_user", job="qa")

# 复杂前置（复用 business 场景）
ctx = user_factory.login_and_get_user(user_id=2)

# DB 造数（需 projects.<项目>.db.enabled=true，并配置连接信息）
user_factory.insert_user_row(name="db_user", email="a@b.com")
```

简单造数可直调单接口；复杂前置优先走 `business` 场景方法。工厂内 `controller` / `name` 须与当前项目 `assets` 一致。

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

日志：控制台输出 **WARNING+**；详细日志（DEBUG+）写入 `logs/framework_YYYYMMDD.log`。

## Pytest 标记

在 `pytest.ini` 中声明；插件通过 `testCases/conftest.py` 的 `pytest_plugins` 注册（含 `single_api_plugin`）。

| 标记 | 含义 |
|------|------|
| `smoke` | 冒烟 |
| `api` | 接口用例 |
| `ui` | UI 用例 |
| `regression` | 回归 |

常量见 `execution/markers.py`。使用 `-m api` / `-m ui` 时，hooks 会跳过另一侧用例树以加快收集。

## Docker

默认只跑 API 用例（镜像未安装 Playwright 浏览器），结果挂载到 `./reports`：

```bash
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
2. 单接口用例 — `testCases/api/FOO/single/*.yaml`
3. `business/api/FOO/*_biz.py` — 只写需要串联的场景方法
4. `datafactory/api/FOO/*_factory.py` — 按需造数（可复用 business）
5. `testCases/api/FOO/scenario/test_*.py` + `data/*.yaml` — 写场景用例与数据
6. UI 同理：`assets/ui/FOO/*.yaml` → `business/ui/FOO` → `testCases/ui/FOO`

保持用例薄、场景可复用、契约与编排分离，便于多项目并行维护。

## 示例工程说明

仓库内置 **AITF** 示例：

- **配置**：`config/test.yaml` 默认指向本地 API（`http://127.0.0.1:8000/`）与 UI（`http://127.0.0.1:5173/`）
- **接口契约**：`assets/api/AITF/` 下多个 View/ViewSet YAML（如 `LoginView`）
- **单接口用例**：`testCases/api/AITF/single/user_login.yaml`（`LoginView` / `post`）
- **场景 / 造数**：`scenario/`、`business`、`datafactory` 中仍有编排模板；其中 `controller` 名须与 assets 保持一致后再启用
- **UI**：`assets/ui/AITF/login.yaml` + `LoginBiz` + `test_login_page.py`；需本地 UI 服务可用