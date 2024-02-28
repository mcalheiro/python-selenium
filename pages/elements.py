from abc import ABC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from page_objects import PageElement


class Task(PageElement):

    name = (By.ID, 'todo-name')
    description = (By.ID, 'todo-desc')
    urgent = (By.ID, 'todo-next')
    submit = (By.ID, 'todo-submit')
    fill_allert = (By.CLASS_NAME, 'terminal-alert-error')

    def create_task(self, name, description, urgent=False):
        self.webdriver.find_element(*self.name).send_keys(name)
        self.webdriver.find_element(*self.description).send_keys(description)
        if urgent:
            self.webdriver.find_element(*self.urgent).click()
        self.webdriver.find_element(*self.submit).click()
    
    def is_filled_correctly(self):
        try:
            self.webdriver.find_element(*self.fill_allert)
            return False
        except NoSuchElementException:
            return True


class CardContainer(PageElement, ABC):
    
    @property
    def todos(self):
        cards = self.find_elements(self.card)
        return [Card(card, self) for card in cards]
    
    def refresh_cards(self):
        cards = self.find_elements(self.card)
        self.cards = [Card(card, self) for card in cards]


class ToDo(CardContainer):

    fieldset = (By.CSS_SELECTOR, 'div.body_a fieldset')
    card = (By.CSS_SELECTOR, '#todo > .terminal-card')


class Doing(CardContainer):

    fieldset = (By.CSS_SELECTOR, 'div.body_b fieldset')
    card = (By.CSS_SELECTOR, '#doing > .terminal-card')


class Done(CardContainer):

    fieldset = (By.CSS_SELECTOR, 'div.body_c fieldset')
    card = (By.CSS_SELECTOR, '#done > .terminal-card')


class Card():
    
    def __init__(self, selenium_obj, container):
        self.selenium_obj = selenium_obj
        self.container = container
        self.name = (By.CSS_SELECTOR, 'header.name')
        self.description = (By.CSS_SELECTOR, 'div.description')
        self._do = (By.CSS_SELECTOR, 'button.do')
        self._cancel = (By.CSS_SELECTOR, 'button.cancel')
        self._load()

    def do(self):
        self.selenium_obj.find_element(*self._do).click()
        self.container.refresh_cards()

    def cancel(self):
        try:
            self.selenium_obj.find_element(*self._cancel).click()
        except NoSuchElementException:
            raise NoSuchElementException('Element has no cancel button')

    def _load(self):
        self.name = self.selenium_obj.find_element(*self.name).text
        self.description = self.selenium_obj.find_element(*self.description).text

    def __repr__(self):
        return f'Card(name="{self.name}", description="{self.description}")'
