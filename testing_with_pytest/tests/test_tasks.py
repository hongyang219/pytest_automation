import pytest
import time
import sys
import requests
from testing_with_pytest.test_data import *
from warnings import warn

#========================================================================#
@pytest.mark.neg
@pytest.mark.parametrize('task', ['Task_100', 'Task_101', 'Task_1000'])
def test_temp_task(task):
    task_name = task
    task_id = task.split('_')[-1]
    print(f'Task: {task_name}, ID: {task_id}')
    assert 'task' in task_name.lower()
    assert int(task_id) % 100 == 0

@pytest.mark.skip(reason="Not implemented")
def test_foobar():
    print(f'This case is skipped')
    assert False

def qual_nothing():
    print(f'This case is None')
    assert False

#========================================================================#
@pytest.mark.func
def test_task_name_and_id(task_params):
    task_name = task_params
    task_id = task_params.split('_')[-1]
    print(f'Task: {task_name}, ID: {task_id}')
    assert 'task' in task_name.lower()
    assert task_id.isdigit()

@pytest.mark.reg
def test_task_name(task_params):
    task_name = task_params
    task_id = task_params.split('_')[-1]
    print(f'Task: {task_name}, ID: {task_id}')
    assert 'task' in task_name.lower()

#========================================================================#
@pytest.mark.file
def test_tmppath_exist(tmp_path):
    print(f'Create temp directory under {tmp_path} through method {sys._getframe().f_code.co_name!r}')
    tmp_dir = tmp_path / "pytest_temp_directory"
    tmp_dir.mkdir()
    assert tmp_dir.exists()

@pytest.mark.file
def test_tmpfile_creation(tmp_path, file_name: str = "pytest-temp-file.txt"):
    print(f'Create temp directory under {tmp_path}\n')
    file_path = tmp_path / file_name
    file_path.write_text(f'Write content to {file_name} through method {sys._getframe().f_code.co_name!r}\n'
                         f'At {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}',
                         encoding='utf-8')
    print(f'Test file: {file_path} created')
    assert file_path.exists()
    assert "content" in file_path.read_text(encoding='utf-8')
    assert "2026" in file_path.read_text(encoding='utf-8')

#========================================================================#
@pytest.mark.cache
def test_cache_upstream():
    assert 1 == 1

@pytest.mark.cache
def test_cache_downstream():
    assert 0 == 1

@pytest.mark.sys
def test_sys_output(capsys):
    def greeting(name):
        if name.isalpha():
            print(f"Hello {name}!")
        elif name.isdigit():
            print(f"{name} is not a name!", file=sys.stderr)
        else:
            print(f"What are you?")
            print(f"Unknown type", file=sys.stderr)

    greeting('Soma')
    out, err = capsys.readouterr()
    assert "Hello Soma!" in out
    assert err == ""

    greeting('219')
    out, err = capsys.readouterr()
    assert out == ""
    assert "not a name!" in err

    greeting('###')
    out, err = capsys.readouterr()
    assert "What are you?" in out
    assert "Unknown type" in err

#========================================================================#
def view_user_info(info = None):
    user_info = info or test_user_info
    user_info = defaultdict(str, user_info)
    return (f'User ID: {user_info['id']}\n'
            f'User Name: {user_info["name"]}\n'
            f'Role: {user_info["role"]}\n'
            f'Title: {user_info["title"]}\n')

def get_response(url: str):
    response = requests.get(url)
    return response

def mock_get(*args, **kwargs):
    mock_response = {'header':'mock head', 'contents':['mock content1', 'mock content2']}
    return mock_response

@pytest.mark.monkey
def test_patch_user_info(monkeypatch):
    title = 'Senior Manager'
    monkeypatch.setitem(test_user_info, 'id', '00000')
    monkeypatch.setitem(test_user_info, 'name', 'Mock User')
    monkeypatch.setitem(test_user_info, 'role', 'Scrum Master')
    monkeypatch.setitem(test_user_info, 'title', title)
    print(view_user_info())
    assert f'Title: {title}' in view_user_info()

@pytest.mark.monkey
def test_delete_user_info(monkeypatch):
    monkeypatch.delitem(test_user_info, 'role')
    print(view_user_info())
    assert not 'role' in test_user_info

@pytest.mark.monkey
def test_get_response(monkeypatch):
    monkeypatch.setattr('requests.get', mock_get)
    response = requests.get('https://fake.url')
    print(f"It's a mocked response:\n  {response}")
    assert not response == 200
    for rv in response.values():
        assert 'mock' in str(rv)

# ========================================================================#
def warning_method():
    msg = 'You are using a deprecated method!!'
    warn(msg, DeprecationWarning)

@pytest.mark.warn
def test_warning_method1(recwarn):
    '''
    Use recwarn fixture to test warning message
    '''
    warning_method()
    assert len(recwarn) == 1
    w = recwarn.pop()
    print('recwarn >>>', w.message)        # recwarn returns a list of warning messages
    assert w.category == DeprecationWarning
    assert 'deprecated' in str(w.message)

@pytest.mark.warn
def test_warning_method2():
    '''
    Use pytest.warns to test warning message
    '''
    with pytest.warns() as warns:
        warning_method()
    assert len(warns) == 1
    w = warns.pop()
    print('pytest.warns() >>>', w.message)        # recwarn returns a list of warning messages
    assert w.category == DeprecationWarning
    assert 'deprecated' in str(w.message)

# ========================================================================#
