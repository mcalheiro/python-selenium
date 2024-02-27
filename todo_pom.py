from selenium.webdriver.common.by import By

class Todo:
    def __init__(self, webdriver):
        """
        Attr = locator
        """
        self.name = (By.ID, 'todo-name')
        self.description = (By.ID, 'todo-desc')
        self.urgent = (By.ID, 'todo-next')
        self.submit = (By.ID, 'todo-submit')
        self.webdriver = webdriver

    def create_task(self, name, description, urgent=False):
        self.webdriver.find_element(*self.name).send_keys(name)
        self.webdriver.find_element(*self.description).send_keys(description)
        if urgent:
            self.webdriver.find_element(*self.urgent).click()
        self.webdriver.find_element(*self.submit).click()

# --------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service()
options = webdriver.ChromeOptions()
webdriver = webdriver.Chrome(service=service, options=options)
url = 'https://selenium.dunossauro.live/todo_list.html'

webdriver.get(url)

todo_page = Todo(webdriver)

todo_page.create_task(
    name='Estudar',
    description='Selenium e python para automacao de testes'
)
