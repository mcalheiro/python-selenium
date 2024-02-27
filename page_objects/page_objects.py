from abc import ABC


class SeleniumObject():

    def find_element(self, locator):
        return self.webdriver.find_element(*locator)

    def find_elements(self, locator):
        return self.webdriver.find_elements(*locator)
    

class Page(SeleniumObject, ABC):
    
    def __init__(self, webdriver, url=''):
        self.webdriver = webdriver
        self.url = url
        self._reflection()
        
    def open(self):
        return self.webdriver.get(self.url)
    
    def _reflection(self):
        for attr in dir(self):
            attr_target = getattr(self, attr)
            if isinstance(attr_target, PageElement):
                attr_target.webdriver = self.webdriver


class PageElement(SeleniumObject, ABC):

    def __init__(self, webdriver=None):
        self.webdriver = webdriver
