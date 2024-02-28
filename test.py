import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from pages.pages import PageToDo

URL = 'https://selenium.dunossauro.live/todo_list.html'
TASK = {'name':'Create a task', 'desc':'Task description'}


@pytest.fixture(scope='function')
def browser():
    service = Service()
    options = webdriver.ChromeOptions()
    chrome_driver = webdriver.Chrome(service=service, options=options)
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture(scope='function')
def todo_page(browser):
    page = PageToDo(browser, URL)
    page.open()
    yield page


@pytest.mark.xfail(reason='Tasks must be given a name')
def test_create_empty_task(todo_page):
    todo_page.task.create_task('', '')
    assert len(todo_page.todo.todos) == 0
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 0
    assert not todo_page.task.is_filled_correctly()

def test_create_task(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    assert len(todo_page.todo.todos) == 1
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 0
    assert todo_page.todo.todos[0].name == TASK['name']


def test_create_urgent_tasks(todo_page):
    tasks = [
        {'name':'Task A', 'desc':'Not urgent', 'urgent':False},
        {'name':'Task B', 'desc':'Urgent', 'urgent':True},
        {'name':'Task C', 'desc':'Urgent', 'urgent':True},
        {'name':'Task D', 'desc':'Not urgent', 'urgent':False},
    ]
    for task in tasks:
        todo_page.task.create_task(task['name'], task['desc'], urgent=task['urgent'])

    assert len(todo_page.todo.todos) == 4
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 0
    assert todo_page.todo.todos[1].name == tasks[1]['name']
    assert todo_page.todo.todos[2].name == tasks[0]['name']
    assert todo_page.todo.todos[3].name == tasks[3]['name']
    assert todo_page.todo.todos[0].name == tasks[2]['name']

def test_do_task_on_todo(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    todo_page.todo.todos[0].do()
    assert len(todo_page.todo.todos) == 0
    assert len(todo_page.doing.todos) == 1
    assert len(todo_page.done.todos) == 0
    assert todo_page.doing.todos[0].name == TASK['name']

def test_finish_task_on_doing(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    todo_page.todo.todos[0].do()
    todo_page.doing.todos[0].do()
    assert len(todo_page.todo.todos) == 0
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 1
    assert todo_page.done.todos[0].name == TASK['name']

def test_redo_task_on_done(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    todo_page.todo.todos[0].do()
    todo_page.doing.todos[0].do()
    todo_page.done.todos[0].do()
    assert len(todo_page.todo.todos) == 1
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 0
    assert todo_page.todo.todos[0].name == TASK['name']

def test_cancel_task_on_todo(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    todo_page.todo.todos[0].cancel()
    assert len(todo_page.todo.todos) == 0
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 0

def test_return_task_on_doing(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    todo_page.todo.todos[0].do()
    todo_page.doing.todos[0].cancel()
    assert len(todo_page.todo.todos) == 1
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 0
    assert todo_page.todo.todos[0].name == TASK['name']

def test_return_task_on_doing(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    todo_page.todo.todos[0].do()
    todo_page.doing.todos[0].cancel()
    assert len(todo_page.todo.todos) == 1
    assert len(todo_page.doing.todos) == 0
    assert len(todo_page.done.todos) == 0
    assert todo_page.todo.todos[0].name == TASK['name']

def test_cancel_task_on_done(todo_page):
    todo_page.task.create_task(TASK['name'], TASK['desc'])
    todo_page.todo.todos[0].do()
    todo_page.doing.todos[0].do()
    with pytest.raises(NoSuchElementException):
        todo_page.done.todos[0].cancel()
