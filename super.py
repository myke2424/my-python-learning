# At a high level, super() gives you access to methods in a parent class from the subclass that inherits from it
# super() alone returns a temporary object of the parent class  that then allows you call that superclass's methods
# A common use case is building classes that extend the functionality of previously built classes.

class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * self.length + 2 * self.width


# Calling super here, lets us take our instance variable length
# and pass it to the width and length values to set on the object
# We need to pass all required init params from the super class to super.__init__() or else it will fail
class Square(Rectangle):
    def __init__(self, length):
        # This is really calling "Rectangle.__init__()"
        # In python3, calling "super()" is equivalent to calling "super(Square, self)"
        super().__init__(width=length, length=length)


# The primary use case of super is to extend the functionality of the inherited method.
# The cube class doesn't need a __init__ method because it inherits it from Square
# The __init__ method of the parent class will be called automatically
class Cube(Square):
    def surface_area(self):
        # I'm extending the functionality of the inherited area method here.
        # This is equivalent to calling "super(Square, self).area()" -> This searches the square class for the area method:wq!
        face_area = super().area()  # We could also call "self.area()" because we inherit the method
        return face_area * 6


# You could reinitialise an object like this, *Not recommended*

class Person:
    def __init__(self, name):
        self.name = name


p = Person('mike')
Person.__init__(p, name='Charlie')  # now  p.name = charlie

r = Rectangle(5, 5)
s = Square(5)

c = Cube(5)
cube_area = c.surface_area()

print()