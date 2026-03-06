# testing_with_pytest

这是一个使用 pytest 进行自动化测试的项目示例，演示了 pytest 的各种特性，包括 fixtures、参数化、标记、临时文件、系统输出捕获、monkeypatch、警告测试等。

## 项目结构

```
testing_with_pytest/
├── conftest.py          # pytest 配置文件，包含 fixtures 和设置
├── test_data.py         # 测试数据和参数定义
├── tests/
│   ├── __init__.py
│   └── test_tasks.py    # 测试用例文件
└── README.md            # 项目说明文档
```

## 依赖项

项目需要以下 Python 包：

- pytest
- selenium
- webdriver-manager
- allure-pytest
- requests

你可以使用以下命令安装依赖：

```bash
pip install pytest selenium webdriver-manager allure-pytest requests
```

## 安装和运行

1. 克隆或下载项目到本地。

2. 进入项目目录：

   ```bash
   cd testing_with_pytest
   ```

3. 运行所有测试：

   ```bash
   pytest
   ```

## 测试说明

### 测试用例

- **test_task_name_and_id**: 使用参数化 fixture 测试任务名称和 ID。
- **test_task_name**: 回归测试任务名称。
- **test_temp_task**: 负向测试案例。
- **test_foobar**: 跳过测试案例。
- **test_tmppath_exist**: 测试临时目录创建。
- **test_tmpfile_creation**: 测试临时文件创建和写入。
- **test_cache_upstream/downstream**: 缓存相关测试。
- **test_sys_output**: 测试系统输出捕获。
- **test_patch_user_info**: 使用 monkeypatch 修改用户信息。
- **test_delete_user_info**: 使用 monkeypatch 删除用户信息。
- **test_get_response**: 模拟网络请求。
- **test_warning_method1/2**: 测试警告消息。

### Fixtures

- **session_fixture**: 会话级别的自动 fixture，用于记录测试开始和结束时间。
- **test_notification**: 函数级别的自动 fixture，用于每个测试的设置和清理。
- **task_params**: 参数化 fixture，提供任务参数。

### 标记 (Marks)

- `@pytest.mark.neg`: 负向测试
- `@pytest.mark.skip`: 跳过测试
- `@pytest.mark.func`: 功能测试
- `@pytest.mark.reg`: 回归测试
- `@pytest.mark.file`: 文件操作测试
- `@pytest.mark.cache`: 缓存测试
- `@pytest.mark.sys`: 系统测试
- `@pytest.mark.monkey`: monkeypatch 测试
- `@pytest.mark.warn`: 警告测试

## 运行特定测试

- 运行功能测试：

  ```bash
  pytest -m func
  ```

- 运行负向测试：

  ```bash
  pytest -m neg
  ```

- 运行单个测试文件：

  ```bash
  pytest tests/test_tasks.py
  ```

- 运行特定测试用例：

  ```bash
  pytest tests/test_tasks.py::test_task_name_and_id
  ```

## 实用 pytest 命令

### 基本命令

- 运行所有测试：

  ```bash
  pytest
  ```

- 详细输出（显示每个测试的执行过程）：

  ```bash
  pytest -v
  ```

- 只收集测试用例，不执行：

  ```bash
  pytest --collect-only
  ```

- 按关键字过滤测试：

  ```bash
  pytest -k "task"
  ```

### 输出和报告

- 简短回溯（默认配置）：

  ```bash
  pytest --tb=short
  ```

- 生成 HTML 报告（已配置为 report.html）：

  ```bash
  pytest --html=report.html
  ```

- 使用表情符号（已配置）：

  ```bash
  pytest --emoji
  ```

- 显示测试执行时间（最慢的10个）：

  ```bash
  pytest --durations=10
  ```

### 控制执行

- 遇到第一个失败后停止：

  ```bash
  pytest --maxfail=1
  ```

- 禁用警告：

  ```bash
  pytest -W ignore
  ```

- 运行特定标记的测试：

  ```bash
  pytest -m "func and not neg"
  ```

### 并行执行（需要安装 pytest-xdist）

- 并行运行测试（例如使用2个进程）：

  ```bash
  pytest -n 2
  ```

### 调试

- 进入调试模式：

  ```bash
  pytest --pdb
  ```

- 失败时进入调试：

  ```bash
  pytest --pdb --maxfail=1
  ```

## 配置

项目使用 `pytest.ini` 文件进行配置（位于父目录 `C:/Soma/codes/pytest_automation`）。

### pytest.ini 配置说明

```ini
[pytest]
;testpaths = pytest_automation/testing_with_pytest/tests

python_functions = test_* qual_*

addopts = -rA --tb=short --html=report.html --emoji --strict-markers

xfail_strict = true

markers =
    func: functional cases
    reg: regression cases
    neg: negative cases
    ...
```

- **python_functions**: 定义测试函数的命名模式（以 `test_` 或 `qual_` 开头的函数被识别为测试）。
- **addopts**: 默认选项，包括 `-rA`（显示所有结果摘要）、`--tb=short`（简短回溯）、`--html=report.html`（生成HTML报告）、`--emoji`（使用表情符号）、`--strict-markers`（严格检查标记）。
- **xfail_strict**: 严格检查 xfail 标记的测试。


## 报告

可以使用 Allure 生成测试报告：

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 贡献
Soma Sun
