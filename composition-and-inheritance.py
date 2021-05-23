# https://realpython.com/inheritance-composition-python/
# Inheritance models "is a relationship"
# E.g. A Car is Vechicle (Class Car extends Vechicle class)

# Composition models "has a relationship" - It enables creating complex types by combing objects of other types
# E.g. a Car is composed of an Engine (Has an engine)
# Composition enables you to resuse code by adding objects to other objects

from abc import ABC, abstractmethod


# ------------ Inheritance examples ------------

# Employee is an abstract base class exists to be inherited, but never instantiated
class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class SalaryEmployee(Employee):
    def __init(self, id, name, weekly_salary):
        # Use super to initialize the members of the base class (Employee)
        super().__init__(id, name)
        self.weekly_salary = weekly_salary

    def calc_payroll(self):
        return self.weekly_salary


class CommisionEmployee(SalaryEmployee):
    def __init__(self, id, name, weekly_salary, commision):
        super().__init__(id, name, weekly_salary)
        self.commision = commision

    def calc_payroll(self):
        # Call salary employee calc payroll implementation
        fixed = super().calc_payroll()
        return fixed + self.commision


# A better way to create an employee abstract base class
# This class cant be instantiated
# This class tells the developers if they inherit EmployeeAbstract, they must override the abstract method
class EmployeeAbstract(ABC):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @abstractmethod
    def calculate_payroll(self):
        pass


# ------------ Composition Examples -------------

# In composition, a class known as composite contains an object of another class known as component
# In other words, a composite class has a component of another class.
# Composition allows composite classes to reuse the implementation of the components it contains.
# The composite class doesn’t inherit the component class interface, but it can leverage its implementation.

# The composition relation between two classes is considered loosely coupled.
# That means that changes to the component class rarely affect the composite class, and changes to the composite class never affect the component class.

# The employee class already uses composition. E.g. - Employee HAS A id, and HAS A name,
# Another attribute might be an address

class Address:
    def __init__(self, street, city, state, zipcode, street2=''):
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zipcode = zipcode


class CompositeEmployee:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.address = None


# You initialize the address attribute to None for now to make it optional, but by doing that, you can now assign an Address to an Employee.
# Composition is a loosely coupled relationship that often doesn’t require the composite class to have knowledge of the component.
# The Employee class leverages the implementation of the Address class without any knowledge of what an Address object is or how it’s represented.
# This type of design is so flexible that you can change the Address class without any impact to the Employee class.