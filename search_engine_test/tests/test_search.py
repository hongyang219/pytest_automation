import pytest
import allure
from selenium.webdriver.common.keys import Keys
import time
from search_engine_test.page_objects import baidu_pageobjects as baidu_po

# 测试数据驱动：搜索 "pytest" 和 "selenium"
@allure.feature("Search")
@allure.story("Baidu")
@pytest.mark.parametrize("search_key", ["python", "selenium"])
def test_baidu_search(browser, search_key):
    """
    :param browser: 从 conftest.py 注入的 webdriver 对象
    :param search_key: 参数化传入的搜索词

    【Summary】
    Test search function

    【Steps】
    1.Open webpage
    2.Locate search bar
    3.Input search key in search bar
    4.Wait for page loading
    5.Assert that the search results containing input search key
    """
    # 1. 打开网页
    url = "https://www.baidu.com"
    with allure.step(f"打开网页: {url}"):
        browser.get(url)

    # 2. 定位搜索框
    # 在实际项目中，这部分应该封装在 Page Object 中
    with allure.step("定位搜索框"):
        search_input = browser.find_element(*baidu_po.baidu_search_bar)

    # 3. 输入关键字并回车
    with allure.step(f"输入关键字 {search_key} 并搜索"):
        search_input.clear()
        search_input.send_keys(search_key)
        search_input.send_keys(Keys.RETURN)

    # 4. 强制等待一小会儿以便页面加载（实际项目推荐用 Explicit Wait）
    time.sleep(2)

    # 5. 断言：验证标题中是否包含搜索关键字
    with allure.step("验证标题包含搜索关键字"):
        assert search_key in browser.title.lower(), (
            f"标题验证失败！预期包含 {search_key}，实际标题为 {browser.title}"
        )

    print(f"搜索 {search_key} 测试通过！")