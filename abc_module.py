# Abstract base classes complement duck-typing by providing a way to define interfaces
# when other techniques like hasattr() would be clumsy or subtly wrong

from abc import ABC, abstractmethod


# Abstract classes are classes that contain one or more abstract methods.
# An abstract method is a method that is declared, but contains no implementation.
# Abstract classes cannot be instantiated, and require subclasses to provide implementations for the abstract methods.

# A helper class that has ABCMeta (ABC) as its metaclass.
# An abstract base class can be created by simply deriving from ABC
class AbstractBaseClass(ABC):

    # Classes that are derived from this class need to implement this abstract method or cant be instantiated
    @abstractmethod
    def some_method(self):
        pass


# A class that is derived from an abstract class cannot be instantiated unless all of its abstract methods are overridden.
# the abstract method can be invoked with super() call mechanism.
# This enables providing some basic functionality in the abstract method, which can be enriched by the subclass implementation.

class Test(AbstractBaseClass):
    def __init__(self):
        self.name = 'im a test'

    def some_method(self):
        return super().some_method()


t = Test()