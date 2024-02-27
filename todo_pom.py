import time
from abc import ABC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SeleniumObject():
    def find_element(self, locator):
        return self.webdriver.find_element(*locator)

    def find_elements(self, locator):
        return self.webdriver.find_elements(*locator)
    

class Page(SeleniumObject, ABC):
    
    def __init__(self, webdriver, url=''):
        self.webdriver = webdriver
        self.url = url
        
    def open(self):
        return self.webdriver.get(self.url)


class PageElement(SeleniumObject, ABC):

    def __init__(self, webdriver):
        self.webdriver = webdriver


class Task(PageElement):

    name = (By.ID, 'todo-name')
    description = (By.ID, 'todo-desc')
    urgent = (By.ID, 'todo-next')
    submit = (By.ID, 'todo-submit')

    def create_task(self, name, description, urgent=False):
        self.webdriver.find_element(*self.name).send_keys(name)
        self.webdriver.find_element(*self.description).send_keys(description)
        if urgent:
            self.webdriver.find_element(*self.urgent).click()
        self.webdriver.find_element(*self.submit).click()


class CardContainer(PageElement, ABC):
    def todos(self):
        cards = self.find_elements(self.card)
        return [Card(card) for card in cards]


class ToDo(CardContainer):

    fieldset = (By.CSS_SELECTOR, 'div.body_a fieldset')
    card = (By.CLASS_NAME, 'terminal-card')


class Doing(CardContainer):

    fieldset = (By.CSS_SELECTOR, 'div.body_b fieldset')
    card = (By.CLASS_NAME, 'terminal-card')


class Done(CardContainer):

    fieldset = (By.CSS_SELECTOR, 'div.body_c fieldset')
    card = (By.CLASS_NAME, 'terminal-card')


class Card():
    
    def __init__(self, selenium_obj):
        self.selenium_obj = selenium_obj
        self.name = (By.CSS_SELECTOR, 'header.name')
        self.description = (By.CSS_SELECTOR, 'div.description')
        self._do = (By.CSS_SELECTOR, 'button.do')
        self._cancel = (By.CSS_SELECTOR, 'button.cancel')
        self._load()

    def do(self):
        self.selenium_obj.find_element(*self._do).click()

    def cancel(self):
        try:
            self.selenium_obj.find_element(*self._cancel).click()
        except NoSuchElementException:
            print('Element has no cancel button')

    def _load(self):
        self.name = self.selenium_obj.find_element(*self.name).text
        self.description = self.selenium_obj.find_element(*self.description).text

    def __repr__(self):
        return f'Card(name="{self.name}", description="{self.description}")'
    

class PageToDo(Page):
    todo = ToDo()
    doing = Doing()
    done = Done()
    task = Task()

# --------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service()
options = webdriver.ChromeOptions()
webdriver = webdriver.Chrome(service=service, options=options)
url = 'https://selenium.dunossauro.live/todo_list.html'

page = PageToDo(webdriver, url)