# PyTestFramework

基于 **Pytest + Requests + Playwright + Allure** 的接口 / UI 自动化测试框架。按 **Application → Domain → Service** 三层组织，支持接口封装、数据驱动、占位符造数、造数工厂、多环境配置与 Jenkins 持续集成。

## 特性

- **API + UI 统一工程**：同一套配置、日志、断言与报告体系
- **接口封装**：`domain/assets/api/<项目>/api_info` 存 YAML 契约；`function/*.py` 封装单接口，底层用 `HttpClient.send`
- **业务层编排**：`domain/business` 串联多接口与可选 DB，暴露场景方法供工厂与用例复用；断言写在 `application/testCases`
- **数据驱动**：支持 YAML / JSON / Excel，配合 `@pytest.mark.parametrize`；加载时自动解析占位符
- **造数工厂**：API 造数 + 可选 MySQL DB 造数；数据文件可用 `{{...}}` / `@{...}` / `${...}` 动态取值
- **Allure 报告**：请求/响应自动附件，UI 失败自动截图
- **多环境 / 多项目**：`service/config/{dev,test,prod}.yaml` 内按 `projects` 分项目；命令行 `ENV` 切换环境
- **CI**：根目录 `Jenkinsfile` 开箱可用；结果通知走企微 / 钉钉 Webhook

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
├── application/                # 应用层：用例入口 + 前置造数
│   ├── testCases/              # 用例（唯一入口）+ 断言 + 用例数据
│   │   ├── api/<项目>/         # API 用例 + data/
│   │   ├── ui/<项目>/          # UI 用例 + data/
│   │   └── conftest.py         # 注册 fixtures / hooks
│   └── datafactory/            # 造数工厂
│       ├── api/<项目>/         # 接口造数（如 user_factory.py）
│       ├── db/                 # 数据库造数（如 user_db_factory.py）
│       └── ui/<项目>/          # UI 造数占位（按需扩展）
├── domain/                     # 领域层：被测系统抽象 + 场景编排
│   ├── assets/                 # 测试资产（不写业务逻辑）
│   │   ├── api/<项目>/
│   │   │   ├── api_info/       # 接口 YAML 契约（如 LoginView.yaml）
│   │   │   └── function/       # 单接口 Python 封装（如 login_view.py）
│   │   └── ui/<项目>/          # 页面元素定位 YAML（按页面命名，如 login.yaml）
│   └── business/               # 业务层（多接口/DB 场景编排；无断言、无单接口透传）
│       ├── api/<项目>/         # 如 user_biz.py（场景方法）
│       └── ui/<项目>/          # 如 login_biz.py（页面操作流程）
├── service/                    # 服务层：与业务无关的自动化核心能力
│   ├── assert_utils/           # 断言工具
│   ├── config/                 # 环境配置加载 + dev/test/prod.yaml
│   ├── data_driver/            # DDT 加载 + 占位符解析
│   ├── database/               # MySQL 客户端
│   ├── http/                   # HttpClient / ApiResponse / auth
│   ├── ui/                     # UiSession / UiPage / UiBizBase / elements_loader
│   ├── logger/                 # loguru 日志
│   ├── utils/                  # 路径工具、random_generator 等
│   ├── execution/              # Pytest 插件层（fixtures / hooks / markers）
│   └── report_ci/              # CI 通知（企微 / 钉钉 Webhook）
├── reports/                    # Allure 结果（运行生成，已 gitignore）
├── logs/                       # 框架日志（运行生成）
├── pytest.ini
├── requirements.txt
└── Jenkinsfile
```

### 分层约定

| 层级 | 目录 | 职责 |
|------|------|------|
| **Application** | `application/testCases`、`application/datafactory` | 用例入口、断言、用例数据、前置造数 |
| **Domain** | `domain/assets`、`domain/business` | 接口/页面原子能力 + 场景编排（无断言） |
| **Service** | `service/*` | HttpClient、UI、DB、配置、断言、fixtures、hooks 等框架能力 |

Domain 层内仍保持上下关系：`business → assets → service`。  
Application 可调用 Domain，也可直接使用 Service 的通用工具（断言、DDT、日志等）。

| 组件 | 职责 | 示例 |
|------|------|------|
| `domain/assets/.../api_info` | 接口契约 YAML | `api_info/LoginView.yaml` |
| `domain/assets/.../function` | 单接口封装 | `function/login_view.py` |
| `domain/assets/ui` | 页面元素定位 | `ui/AITF/login.yaml` |
| `HttpClient.send` | 直传 method/url 发请求 | `client.send("POST", "/api/auth/login/", ...)` |
| `domain/business` | 多接口串联 / 可选 DB 的场景编排（不含断言） | `create_user(...)` |
| `application/datafactory` | 前置造数（单接口直调或复用 business） | `user_factory.create_user()` |
| `application/testCases` | 调接口封装 / business + 断言 | `test_user.py`、`test_login_page.py` |
| `service`（含 `execution`） | 框架能力，一般不改业务代码 | HttpClient、fixtures、hooks |

```text
application/testCases ──┬── api/*.py  → domain assets function / Business.scenario(...)
                        └── ui/*.py   → Business UI + 断言
application/datafactory ──┬── 简单造数 → domain assets function
                          └── 复杂前置 → Business.scenario(...)
domain/business ─────────────────→ domain assets function + DatabaseClient
service/HttpClient ──────────────→ send(method, url, ...) → ApiResponse
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

环境配置统一写在 `service/config/*.yaml`（如 `dev.yaml`、`test.yaml`），启动时按 `ENV` 加载对应文件。

说明：

- 默认 `ENV=test`，即加载 `service/config/test.yaml`
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
pytest application/testCases/api/AITF
pytest application/testCases/api/AITF/test_user.py
pytest application/testCases/ui/AITF/test_login_page.py

# 并行（需 pytest-xdist）
pytest -n auto -m api

# 失败立刻重试（pytest-rerunfailures，同一轮内失败后再试 N 次）
pytest --reruns 1 -m api

# 只重跑上一轮失败用例（pytest 内置，跨轮次）
# 例：全量 1000 条失败 30 条 → 下一轮只跑这 30 条
pytest --lf
# 失败优先：先跑上次失败的，再跑其余
pytest --ff
# 可组合：只重跑失败项，且每个失败再即时重试一次
pytest --lf --reruns 1
```

### 4. 查看 Allure 报告

Allure 原始结果固定写到**项目根** `reports/allure-results`（由 `pytest_configure` 按 `PROJECT_ROOT` 定位，不依赖启动时的 cwd）：

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 配置说明

配置按「运行环境 × 项目」组织：先用 `ENV` 选择 `service/config/{ENV}.yaml`，再按用例路径中的项目名（如 `application/testCases/api/AITF/...` → `AITF`）加载 `projects.<项目>`，并与 `defaults` 深度合并。

`service/config/test.yaml` 示例：

```yaml
env: test
defaults:
  timeout: 10
  ui:
    headless: false             # pytest fixture 浏览器有头/无头
    default_timeout: 10
    navigation_timeout: 30
notify:
  enabled: true
  title: PyTestFramework
  msgtype: markdown
  mention_all_on_fail: false
  max_failed_list: 10
  report_url: ""
  wecom:                        # 企业微信通道
    webhook: ""
  dingtalk:                     # 钉钉通道（可与企微同时开启）
    webhook: ""
    secret: ""
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
    global_var:                 # 项目级公共变量（数据文件可用 ${user} 引用）
      user: admin
      password: 123456
    notify:                     # 可选：覆盖/补充该项目的通道
      wecom:
        webhook: ""
      dingtalk:
        webhook: ""
        secret: ""
# OtherApp:
#   api_base_url: https://other-api.example
#   notify:
#     wecom:
#       webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
#     dingtalk:
#       webhook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
#       secret: SECxxx
```

| 配置项 | 说明 |
|--------|------|
| `defaults.*` | 各项目共用的默认值（超时、UI 等） |
| `defaults.ui.headless` | pytest / testCases 浏览器有头/无头 |
| `projects.<项目>.api_base_url` | 该项目 API 根地址 |
| `projects.<项目>.ui.base_url` | 该项目 UI 入口地址 |
| `projects.<项目>.db` | 该项目数据库连接（按项目配置，无 defaults） |
| `projects.<项目>.global_var` | 项目级公共变量 |
| `projects.<项目>.timeout` / `ui` | 可覆盖 defaults 中同名项 |
| `projects.<项目>.notify` | 项目级通知（与全局 deep merge；可同时配企微+钉钉） |
| `notify.enabled` | 总开关（无任何通道 webhook 时仍会跳过） |
| `notify.wecom.webhook` | 企业微信群机器人 Webhook |
| `notify.dingtalk.webhook` | 钉钉群机器人 Webhook |
| `notify.dingtalk.secret` | 钉钉加签密钥（可选） |
| `notify.report_url` | 报告链接（写入通知正文） |

新增项目时：在 `projects` 下增加同名段，并保持目录约定  
`application/testCases/api|<ui>/<项目>/`、`domain/assets/.../<项目>/`、`domain/business/api|<ui>/<项目>/`。

可选环境变量：

- `NOTIFY_WECOM_WEBHOOK` / `NOTIFY_DINGTALK_WEBHOOK` / `NOTIFY_DINGTALK_SECRET` → 覆盖全局通道
- `NOTIFY_AITF_WECOM_WEBHOOK` / `NOTIFY_AITF_DINGTALK_WEBHOOK` 等 → 覆盖项目通道
- `NOTIFY_ENABLED` / `NOTIFY_REPORT_URL` / `NOTIFY_MENTION_ALL_ON_FAIL` → 通知总开关与公共项
- `UI_HEADLESS` → 覆盖 `defaults.ui.headless`（`1` / `true` / `yes`）
- `PROJECT=AITF` 时，下列变量只覆盖该项目；未指定 `PROJECT` 则覆盖配置中全部项目：
  - `API_BASE_URL` → `api_base_url`
  - `UI_BASE_URL` → `ui.base_url`
  - `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` → `db.*`

## 编写 API 用例

用例写在 `application/testCases/api/<项目>/test_*.py`，通过 `domain/assets` 接口封装或 `domain/business` 编排，断言写在用例里；数据文件放同级 `data/`。

### 1. 接口契约与封装

- `domain/assets/api/<项目>/api_info/*.yaml`：接口契约（method / url / body 等）
- `domain/assets/api/<项目>/function/*.py`：按契约封装的单接口调用类，内部调用 `HttpClient.send`；路径参数用 `path_params` 替换 `{id}`

```python
from domain.assets.api.AITF.function import LoginView

resp = LoginView().post(account=account, password=password)
# ApiResponse 行为像 dict：resp["token"]；同时有 resp.status_code / resp.body
token = resp["token"]
```

底层也可直接：

```python
resp = http_client.send(
    "POST",
    "/api/auth/login/",
    name="LoginView.post",
    json={"account": account, "password": password},
)
```

返回值为 `ApiResponse`：响应体是对象时可直接 `resp["token"]` / `resp.get("id")`；HTTP 状态码用 `resp.status_code`；原始 body（含 list/str）用 `resp.body`。鉴权头可用 `authorization_value(token)`（默认 `Token <token>`）。

### 2. 业务场景编排（非单接口透传）

`domain/business/api/<项目>/*_biz.py` 只写多接口串联 / 可选 DB 的场景，供工厂与用例复用，**不做断言**。

```python
from domain.assets.api.AITF.function import LoginView, UserViewSet

def create_user(account: str, username: str, email: str, password: str):
    token = LoginView().post(account="admin", password="123456")["token"]
    return UserViewSet().create(
        token=token, account=account, username=username, email=email, password=password
    )
```

### 3. 用例 + 数据驱动

用例文件：`application/testCases/api/<项目>/test_*.py`  
数据文件：放在同级 `data/` 下（如 `data/user.yaml`），`parametrize_data` 只需传文件名。

```python
from domain.business.api.AITF.user_biz import create_user
from service.assert_utils import AssertUtils
from service.data_driver import parametrize_data

@pytest.mark.parametrize("case", parametrize_data("user.yaml"))
def test_user_add(case):
    resp = create_user(case["account"], case["username"], case["email"], case["password"])
    AssertUtils.status_code(resp, case["assert"]["status_code"])
```

`application/testCases/api`、`application/testCases/ui` 下的用例会自动打上 `pytest.mark.api` / `pytest.mark.ui`，以及 Allure Feature `API` / `UI`，用例里不必再写。

内置 fixture：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `project_name` | function | 从用例路径解析项目名 |
| `project_config` | function | 当前项目合并后的配置 |
| `http_client` | function | 按项目缓存的 `HttpClient` |
| `env_config` | session | 当前环境完整配置 |
| `db` | function | 按项目的 `DatabaseClient`（未启用时为 no-op） |
| `user_factory` | function | AITF 造数模块（`create_user` / `get_admin_token`） |

## 编写 UI 用例

### 1. 元素定位

`domain/assets/ui/<项目>/<页面>.yaml`：只存 selector。支持扁平键，或包在 `elements:` 下。

```yaml
account: "#account"
password: "#password"
show_password: "[aria-label='Show']"
submit: "button[type='submit']"
message: ".ant-message"
```

通用操作在 `service.ui.UiPage`（`open` / `type` / `click` / `text_of` / `locator`）。业务类通常继承 `UiBizBase`。

### 2. 业务层

`domain/business/ui/<项目>/login_biz.py` 用 `UiBizBase` + `UiPage` 封装页面操作流程，不做断言。支持双模式：

- **pytest 注入**：`LoginBiz(page)`，有头/无头由 `defaults.ui.headless` 决定
- **独立运行**：`LoginBiz(project="AITF")`，自启 `UiSession`（固定有头）；结束调用 `biz.close()`

```python
from domain.business.ui.AITF.login_biz import LoginBiz

# 不经 pytest（调试）
biz = LoginBiz(project="AITF")
try:
    biz.login("admin", "123456")
finally:
    biz.close()
```

### 3. 用例

`application/testCases/ui/conftest.py` 会自动：打 `ui` 标记、Allure Feature=`UI`，并在每条用例前 `page.goto(ui_base_url)`。

```python
from domain.business.ui.AITF.login_biz import LoginBiz
from service.assert_utils import AssertUtils
from service.data_driver import parametrize_data

@allure.story("登录页面测试")
@pytest.mark.parametrize("case", parametrize_data("login_cases.yaml"))
def test_login_page(page, case):
    biz = LoginBiz(page)
    biz.login(case["username"], case["password"])
    if case.get("expect"):
        AssertUtils.equal(page.url, case["expect"])
```

数据文件放在用例同级 `data/`（如 `application/testCases/ui/AITF/data/login_cases.yaml`）。

内置 UI fixture：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `ui_base_url` | function | 当前项目的 UI 地址（未配置则报错） |
| `playwright_instance` | session | Playwright 实例 |
| `browser` | session | Chromium（`defaults.ui.headless`，最大化窗口） |
| `page` | function | 独立 context + page；超时取当前项目 UI 配置 |

失败时 `service/execution/hooks/pytest_hooks.py` 会自动截图并附加到 Allure（带 `api` 标记或无 `page` 时跳过）。

## 数据驱动与占位符

`service.data_driver.parametrize_data` 支持：

- `.yaml` / `.yml`：默认取文档中的 `cases` 列表
- `.json`：同上
- `.xlsx` / `.xls`：首行为表头，返回 `list[dict]`

路径约定：只传文件名时，自动加载**调用方用例同级** `data/<文件名>`（如 `application/testCases/api/AITF/data/user.yaml`、`application/testCases/ui/AITF/data/login_cases.yaml`）。仍兼容绝对路径，以及相对项目根 / `application/testCases/` 的路径。

加载后自动解析占位符（`service/data_driver/placeholder.py`）：

| 写法 | 含义 | 示例 |
|------|------|------|
| `{{name}}` / `{{name(...)}}` | 调用 `service.utils.random_generator` 同名方法（无参可省略 `()`） | `{{generate_email}}`、`{{generate_string(prefix='user_')}}` |
| `@{path}` / `@{path()}` | 调用 `application.datafactory` 下对应路径方法 | `@{api.AITF.create_user}` |
| `${key}` | 读取当前项目 `global_var` | `${user}` |

常用随机方法：`generate_string`、`generate_email`、`generate_chinese_name`、`generate_english_name`、`generate_phone`、`generate_id_card`、`generate_integer`、`generate_date`、`generate_today`、`generate_timestamp`。

YAML 示例（见 `application/testCases/api/AITF/data/user.yaml`）：

```yaml
cases:
  - name: create_user_success
    account: {{generate_string(prefix='user_')}}
    username: {{generate_chinese_name}}
    email: {{generate_email}}
    password: 123456
    assert:
      status_code: 201
```

## 造数工厂

API 造数放在 `application/datafactory/api/<项目>/`；DB 造数放在 `application/datafactory/db/`。简单造数可直调 `domain/assets`；复杂前置优先复用 `domain/business`。

```python
# fixture user_factory 返回 application.datafactory.api.AITF.user_factory 模块
token = user_factory.get_admin_token()
body = user_factory.create_user()   # 内部复用 business.create_user + 随机账号

# DB 造数（需 projects.<项目>.db.enabled=true）
from application.datafactory.db.user_db_factory import UserDbFactory

db_factory = UserDbFactory(db)
db_factory.insert_user(name="db_user", email="a@b.com")
db_factory.delete_user_by_email("a@b.com")
```

## 断言与日志

```python
from service.assert_utils import AssertUtils
from service.logger import logger

AssertUtils.status_code(resp, 200)
AssertUtils.equal(actual, expected)
AssertUtils.contains(body, "token")
AssertUtils.json_path_equals(body, "$.data.id", 1)
AssertUtils.json_path_exists(body, "$.data.id")
AssertUtils.true(condition, "说明")

logger.info("自定义日志")
```

日志：控制台输出 **WARNING+**；详细日志（DEBUG+）写入 `logs/framework_YYYYMMDD.log`。

## Pytest 标记

在 `pytest.ini` 中声明；插件通过 `application/testCases/conftest.py` 的 `pytest_plugins` 注册。

| 标记 | 含义 |
|------|------|
| `smoke` | 冒烟 |
| `api` | 接口用例 |
| `ui` | UI 用例 |
| `regression` | 回归 |

常量见 `service/execution/markers.py`。使用 `-m api` / `-m ui` 时，hooks 会跳过另一侧用例树以加快收集。

## 结果通知（企业微信 / 钉钉）

企微和钉钉是 **`notify` 下的两个通道**，可同时开启；再按项目拆分结果推送到各自群：

```yaml
notify:
  enabled: true
  title: PyTestFramework
  wecom:
    webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default"
  dingtalk:
    webhook: "https://oapi.dingtalk.com/robot/send?access_token=default"
    secret: "SECxxx"

projects:
  AITF:
    notify:                         # 与全局 deep merge；可只改其中一个通道
      wecom:
        webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aitf"
      dingtalk:
        webhook: "https://oapi.dingtalk.com/robot/send?access_token=aitf"
        secret: "SECaitf"
  OtherApp:
    notify:
      wecom:
        webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=other"
```

```bash
set NOTIFY_AITF_WECOM_WEBHOOK=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aitf
set NOTIFY_AITF_DINGTALK_WEBHOOK=https://oapi.dingtalk.com/robot/send?access_token=aitf
set NOTIFY_AITF_DINGTALK_SECRET=SECaitf

pytest -m api
```

只要通道配了 `webhook` 就会发送；两个都配则企微和钉钉各发一条。本地不想打扰：`NOTIFY_ENABLED=false`，或保持 webhook 为空。

## Jenkins

`Jenkinsfile` 流水线阶段：

1. Checkout
2. Setup（venv + 依赖 + Playwright Chromium）
3. Test（`pytest -m "api or ui"`）
4. Allure Report
5. Notify（pytest 会话结束钩子已发详情；`NOTIFY_PIPELINE=1` 时可再发流水线级通知）
6. 归档 `reports/**`

配置 Jenkins 凭据 / 环境变量后，将 `NOTIFY_WECOM_WEBHOOK` / `NOTIFY_DINGTALK_WEBHOOK`（及 `NOTIFY_DINGTALK_SECRET`）、`UI_BASE_URL` 等注入即可。用例跑完后由 `pytest_terminal_summary` 自动汇总通过/失败并推送到企微或钉钉。兼容旧变量 `NOTIFY_WEBHOOK`。

## 扩展新项目（建议步骤）

以新增项目 `FOO` 为例：

1. `domain/assets/api/FOO/api_info/*.yaml` — 写接口契约
2. `domain/assets/api/FOO/function/*.py` — 写单接口封装
3. `domain/business/api/FOO/*_biz.py` — 只写需要串联的场景方法
4. `application/datafactory/api/FOO/*_factory.py` — 按需造数（可复用 business）
5. `application/testCases/api/FOO/test_*.py` + `data/*.yaml` — 写用例与数据
6. UI 同理：`domain/assets/ui/FOO/*.yaml` → `domain/business/ui/FOO` → `application/testCases/ui/FOO`
7. 在 `service/config/*.yaml` 的 `projects` 下增加 `FOO` 配置段

保持用例薄、场景可复用、接口封装与编排分离，便于多项目并行维护。

## 示例工程说明

仓库内置 **AITF** 示例：

- **配置**：`service/config/test.yaml` 默认指向本地 API（`http://127.0.0.1:8000/`）与 UI（`http://127.0.0.1:5173/`）
- **契约 / 封装**：`domain/assets/api/AITF/api_info/` + `function/`（如 `LoginView`、`UserViewSet`）
- **API 用例**：`application/testCases/api/AITF/test_user.py` + `data/user.yaml`（含占位符造数）
- **场景 / 造数**：`domain/business/api/AITF/user_biz.py`、`application/datafactory/api/AITF/user_factory.py`、`application/datafactory/db/user_db_factory.py`
- **UI**：`domain/assets/ui/AITF/login.yaml` + `LoginBiz` + `test_login_page.py` + `data/login_cases.yaml`；需本地 UI 服务可用
