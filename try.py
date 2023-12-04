from abc import ABC, abstractmethod

class BaseClass(ABC):

    def foo():
        print('some')

class ChildClass(BaseClass):
    def foo1():
        print('ok')

a = BaseClass()