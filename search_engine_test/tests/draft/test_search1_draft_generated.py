import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from search_engine_test.page_objects.baidu_pageobjects import baidu_search_bar

@pytest.mark.parametrize("fruit", ["apple", "banana", "orange", "grape", "watermelon"])
def test_baidu_search_fruits(browser, fruit):
    """
    Test search function with various fruits.
    """
    # Step 1: Navigate to target page - www.baidu.com
    browser.get("https://www.baidu.com")

    # Step 2: Locate search bar
    search_bar = browser.find_element(*baidu_search_bar)

    # Step 3: Input search key in search bar and search
    search_bar.send_keys(fruit)
    search_bar.send_keys(Keys.RETURN)

    # Step 4: Wait for page loading
    WebDriverWait(browser, 10).until(EC.title_contains(fruit))

    # Step 5: Assert that the search results containing input search key
    assert fruit in browser.title, f"Search results title does not contain {fruit}"