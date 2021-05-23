# Descriptors give us a powerful technique to write reusable code that can be shared between classes.

# Some background information...
# When you access an attribute of an object like "mycircle.radius",
# you're getting back a value stored in a dict on the object

# E.g. mycircle.radius -> mycircle.__dict__['radius'] (attribute access is syntatic sugar for dict look up)
# If you look up a object attribute and it can't be found, it then looks at the class attributes e.g. type(obj).__dict__
# Class attributes are also stored in a dict, e.g. Circle.__dict__ -> {"PI": 3.14}


# The following is a broken python code, the circumference doesn't reflect the change in radius

class Circle:
    PI = 3.14

    def __init__(self, radius):
        self.radius = radius
        self.circumference = 2 * radius * self.PI


c = Circle(2)
c.radius = 3
print(c.circumference)  # Prints 12.56 -> Should print 18.14


# We can fix this with the property decorator (Remember this is just a method call)
# But is this the right solution...?
class Circle2:
    PI = 3.14

    def __init__(self, radius):
        self.radius = radius

    @property
    def circumference(self):
        return 2 * self.radius * self.PI


# What's a descriptor?
# A descriptor is any object that implements at least one of methods named:
# __get__(), __set__() and __delete__()

# What's a data descriptor?
# A data descriptor implements both __get__() and __set(), implementing only __get__() makes you a non-data descriptor.

# Accessing an attribute on an object, e.g -> obj.foo gets you:
# 1. The result of the __get__ method of the data descriptor of the same name attached to the class if it exists.
# 2. Or the corresponding value in obj.__dict__ if it exists
# 3. Or the result of the __get__ method of the non-data descriptor of the same name on the class.
# 4. Or else it falls back to look in the type(obj).__dict__ (the class attributes)
# 5. Repeating for each type in the MRO (inheritance chain) until it finds a match
# 6. And assignment always creates an entry in obj.__dict__


# Descriptor Example 1

# The Ten class is a descriptor that always returns the constant 10 from its __get__ method
class Ten:
    def __get__(self, obj, obj_type=None):
        return 10


# To use the descriptor, it must be stored as a class variable in another class:

class A:
    x = 5
    y = Ten()


# What's the difference between the 'x' and 'y' attribute lookups?
# In the a.x attribute lookup, the dot operator finds the key x and the value 5 in the class dict -> type(obj).__dict__
# In the a.y attribute lookup, the dot operator finds a descriptor instance, recognized by its __get__ method and calls that method which returns 10
# The value 10 isn't stored in the instance/class dict, its computed on demand.
# This isn't really a useful example though, for retrieving constants, regular attribute access is sufficient.

a = A()
a.x  # 5
a.y  # 10

# Descriptor Example 2
import os


# Descriptors typically run computations instead of returning constants
# This lookup is dynamic, it will compute different updated answers each time

class DirectorySize:
    def __get__(self, obj, obj_type=None):
        return len(os.listdir(obj.dirname))


class Directory:
    size = DirectorySize()

    def __init__(self, dirname):
        self.dirname = dirname


# The above descriptor is the same as using the property decorator...  but yo
class D:
    def __init__(self, dirname):
        self.dirname = dirname

    @property
    def size(self):
        return len(os.listdir(self.dirname))


# Example 3:
# A popular use case for descriptors is managing access to instance data.
# The descriptor is assigned to a public attr in the class dict while the actual data is stored as a private attr in the instance ict.

# In the following example, age is the public attribute and _age is the private attribute.
# When the public attr is accessed, the descriptor logs the lookup or update.

import logging

logging.basicConfig(level=logging.INFO)


# __get__ is kind of like a decorator in a sense, you're wrapping attribute lookup with some additional behaviour, in this case its logging the lookup.
# It's "intercepting" attribute lookup
class LoggedAgeAccess:
    def __get__(self, obj, obj_type=None):
        value = obj._age
        logging.info('Accessing %r giving %r', 'age', value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', 'age', value)
        obj._age = value


class Person:
    age = LoggedAgeAccess()  # Descriptor Instance

    def __init__(self, name, age):
        self.name = name  # Regular instance attribute
        self.age = age  # Calls __set__ from the descriptor instance

    def birthday(self):
        self.age += 1  # Calls both __get__ and __set__


# The actual data is in a private attribute
p = Person('mike', 25)
vars(p)  # {'name': 'mike', '_age': 26}

p.birthday()

# When you access/update the age attr it logs this:
# INFO:root:Accessing 'age' giving 25
# INFO:root:Updating 'age' to 26

# Example 4 : Practical Validator Example
# A validator is a descriptor for managed attribute access. Prior to storing any data, it verifies that the new value meets various type and range restrictions.
# If those restrictions aren’t met, it raises an exception to prevent data corruption at its source.

from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')


class Number(Validator):

    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )


class String(Validator):

    def __init__(self, minsize=None, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(
                f'Expected {self.predicate} to be true for {value!r}'
            )


# This is a cleaner way of validating instead of having a large constructor with validation logic
# The descriptors prevent invalid instances from being created
# Descriptors are more for people who are creating their own APIs or writing Python internals
class Component:
    name = String(minsize=3, maxsize=10, predicate=str.isupper)
    kind = OneOf('wood', 'metal', 'plastic')
    quantity = Number(minvalue=0)

    def __init__(self, name, kind, quantity):
        self.name = name
        self.kind = kind
        self.quantity = quantity
