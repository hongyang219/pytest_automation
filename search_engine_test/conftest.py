import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# @pytest.fixture 是 Pytest 的核心
# scope="function" 表示每个测试用例都会执行一次这个 setup/teardown
# 如果想整个测试过程只启动一次浏览器，可以改为 scope="session"
@pytest.fixture(scope="function")
def browser(request):
    print("\n[Setup] 正在启动 Chrome 浏览器...")
    # 使用 WebDriver Manager 自动管理驱动
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # 如果需要无头模式可开启

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)  # 隐式等待
    driver.maximize_window()

    # yield 之前是 Setup 部分，yield 之后是 Teardown 部分
    # 将 driver 暴露给报告钩子，失败时便于截图
    request.node._driver = driver

    yield driver

    print("\n[Teardown] 测试结束，关闭浏览器...")
    # 如果用例失败，附加截图到 Allure 报告
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            # 避免因为截图异常导致 teardown 失败
            pass

    driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    让每个阶段的测试结果可被 fixture 访问，便于失败时截图。
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)