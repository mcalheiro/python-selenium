from page_objects import Page
from .elements import ToDo, Doing, Done, Task

class PageToDo(Page):
    todo = ToDo()
    doing = Doing()
    done = Done()
    task = Task()
