from time import strftime

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import time
from test_data import *

@pytest.fixture(autouse=True, scope='session')
def session_fixture():
    now = time.localtime(time.time())
    print(f'RUN SETUP')
    print(f'Session started at {time.strftime('%Y-%m-%d %H:%M:%S', now)}')
    yield
    now = time.localtime(time.time())
    print(f'Session ended at {time.strftime('%Y-%m-%d %H:%M:%S', now)}')
    print(f'RUN TEARDOWN')

@pytest.fixture(autouse=True, scope='function')
def test_notification():
    print(f'TEST SETUP')
    yield
    print(f'TEST TEARDOWN')

def generate_task_id(fixture_value):
    # Generate task id for each task
    return "t"+fixture_value[-1]

@pytest.fixture(name='task_params', scope='function', params=tasks, ids=generate_task_id)
def task_fixture_for_passing_params(request):
    print(f'FIXTURE START: {sys._getframe().f_code.co_name!r}')
    yield request.param
    print(f'FIXTURE END')