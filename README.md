# PyTestFramework

基于 **Pytest + Requests + Playwright + Allure** 的接口 / UI 自动化测试框架。按「资产 → 业务 → 用例」分层，支持 YAML 接口契约、数据驱动、造数工厂、多环境配置与 Jenkins / Docker 持续集成。

## 特性

- **API + UI 统一工程**：同一套配置、日志、断言与报告体系
- **YAML 接口契约**：`assets/api/<项目>/*.yaml` 定义 controller / method / url，用例侧按契约发起请求
- **业务层封装**：`business` 组合接口与页面动作并暴露方法；断言写在 `testCases`
- **数据驱动**：支持 YAML / JSON / Excel，配合 `@pytest.mark.parametrize`
- **造数工厂**：API 造数 + 可选 MySQL DB 造数
- **Allure 报告**：请求/响应自动附件，UI 失败自动截图
- **多环境**：`config/{dev,test,prod}.yaml` + `.env` 覆盖
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
├── business/                   # 业务层（组合资产，封装场景调用；无断言）
│   ├── api/<项目>/             # 如 user_biz.py
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
├── Jenkinsfile
└── .env.example
```

### 分层约定

| 层级 | 职责 | 示例 |
|------|------|------|
| `assets` | 接口契约、页面元素与操作 | `UserController.yaml`、`LoginPage` |
| `business` | 场景调用封装，供工厂与用例复用（不含断言） | `UserBiz.login()`、`LoginBiz.login()` |
| `datafactory` | 前置造数（可调用 business） | `UserDataFactory.create_user()` |
| `testCases` | 场景编排 + 断言 | `test_user_login.py` |
| `core` / `execution` | 框架能力，一般不改业务代码 | HttpClient、fixtures |

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

```bash
cp .env.example .env
```

按需修改 `.env` 或对应 `config/*.yaml`：

```bash
ENV=test
# BASE_URL=https://reqres.in
# UI_BASE_URL=https://your-ui-host.example
# UI_HEADLESS=true
# DB_HOST=127.0.0.1
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=secret
# DB_NAME=testdb
# NOTIFY_WEBHOOK=
```

说明：

- `ENV` 决定加载 `config/{ENV}.yaml`（默认 `test`）
- 环境变量优先级高于 YAML，可覆盖 `BASE_URL`、`UI_*`、`DB_*`、`NOTIFY_WEBHOOK`
- 跑 UI 用例前必须配置 `ui.base_url` 或 `UI_BASE_URL`，否则会抛出 `UsageError`

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

`config/test.yaml` 示例：

```yaml
env: test
base_url: https://reqres.in
timeout: 10
ui:
  base_url: ""
  headless: true
  default_timeout: 10
  navigation_timeout: 30
db:
  enabled: false
  host: 127.0.0.1
  port: 3306
  user: root
  password: ""
  database: testdb
notify:
  webhook: ""
```

| 配置项 | 说明 |
|--------|------|
| `base_url` | API 根地址 |
| `timeout` | HTTP 默认超时（秒） |
| `ui.base_url` | UI 入口地址 |
| `ui.headless` | Playwright 是否无头 |
| `db.enabled` | 是否启用 MySQL（造数用） |
| `notify.webhook` | 钉钉 / 企微类 webhook |

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

请求时通过 `(controller, url)` 定位契约；路径参数用 `path_params` 替换 `{id}`。

### 2. 封装业务

`business/api/<项目>/user_biz.py`：

```python
class UserBiz:
    CONTROLLER = "UserController"

    def login(self, email: str, password: str) -> requests.Response:
        return self.client.request(
            self.CONTROLLER,
            "/api/login",
            json={"email": email, "password": password},
        )
```

业务层只负责调用与返回结果，**不做断言**；数据工厂与用例均可复用这些方法。

### 3. 编写用例 + 数据驱动

用例文件：`testCases/api/<项目>/test_*.py`  
数据文件：建议放在同级 `DDT/` 或用例相对路径下，并通过 `parametrize_data` 加载（路径相对 `testCases/`）。

```python
@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize("case", parametrize_data("api/AITF/DDT/login_cases.yaml"))
def test_user_login(http_client, user_factory, case):
    biz = UserBiz(http_client)
    resp = biz.login(email, password)
    AssertUtils.status_code(resp, 200)
    AssertUtils.contains(resp.json(), "token")
```

内置 fixture：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `http_client` | session | `HttpClient` 实例 |
| `env_config` | session | 当前环境配置 |
| `db` | session | `DatabaseClient`（未启用时为 no-op） |
| `user_factory` | function | `UserDataFactory` |

## 编写 UI 用例

### 1. Page Object

`assets/ui/pages/login_page.py` 继承 `BasePage`，只封装定位与基础操作。

### 2. 业务层

`business/ui/login_biz.py` 组合页面动作并返回结果，不做断言。

### 3. 用例

```python
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.parametrize("case", parametrize_data("ui/AITF/data/login_cases.yaml"))
def test_login_page(page, ui_base_url, case):
    biz = LoginBiz(page, ui_base_url)
    msg = biz.login(case["username"], case["password"])
    AssertUtils.contains(msg, "Login success")
```

内置 UI fixture：

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `ui_base_url` | session | 读取配置中的 UI 地址 |
| `browser` | session | Chromium 浏览器 |
| `page` | function | 独立 context + page；用例结束自动关闭 |

失败时 `execution/hooks/pytest_hooks.py` 会自动截图并附加到 Allure。

## 数据驱动

`core.data_driver.parametrize_data` 支持：

- `.yaml` / `.yml`：默认取文档中的 `cases` 列表
- `.json`：同上
- `.xlsx` / `.xls`：首行为表头，返回 `list[dict]`

路径解析顺序：绝对路径 → 相对项目根 → `testCases/<path>`。

## 造数工厂

```python
# API 造数
user = user_factory.create_user(name="factory_user", job="qa")

# DB 造数（需 config 中 db.enabled=true，并配置连接信息）
user_factory.insert_user_row(name="db_user", email="a@b.com")
```

工厂内部可复用 `business`，避免用例里散落造数细节。

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

1. `assets/api/FOO/*.yaml` — 写接口契约  
2. `business/api/FOO/*_biz.py` — 封装业务  
3. `datafactory/api/FOO/*_factory.py` — 按需造数  
4. `testCases/api/FOO/test_*.py` + `DDT/*.yaml` — 写用例与数据  
5. UI 同理：`assets/ui/pages` → `business/ui` → `testCases/ui/FOO`

保持用例薄、业务可复用、契约与实现分离，便于多项目并行维护。

## 示例工程说明

仓库内置 **AITF** 示例，对接 [ReqRes](https://reqres.in) 演示 API 登录 / 造数；UI 登录页为 Page Object 模板，需自行配置真实 `UI_BASE_URL` 后验证。

## License

Internal use / 按团队约定。
