# Polymorphism means having MANY FORMS! This means, objects with that share a method (through inheritance) can have a
# different implementation (method overriding)

# Polymorphism is about having only one callable behaviour, but having this behaviour be different for different
# entities (such as two objects both providing the add() method, but both having it do different things.)

# ------------- Example of polymorphic functions -------------
# There are some functions in Python which are compatible to run with multiple data types.
# The len() function would be a polymorphic function (can operate on different types of data)

# ------------- Example of polymorphism with class methods -------------
class Canada:
    @staticmethod
    def language():
        print('english')


class Japan:
    @staticmethod
    def language():
        print('japanese')


c = Canada()
j = Japan()

# Both have the same method with a different implantation, this is polymorphic behaviour
for country in [c, j]:
    country.language()


# ------------- Example of polymorphism with Inheritance -------------
# Polymorphism lets us define methods in the child class that have the same name as the methods in the parent class

class Animal:
    def sound(self):
        print('Random animal sound')


class Dog(Animal):
    # Override the method for different behaviour
    def sound(self):
        print('Woof')


class Cat(Animal):
    def sound(self):
        print('Meow')


d = Dog()
c = Cat()

# Different implementation of the same method
for animal in [d, c]:
    animal.sound()