# Theirs a pattern with the double underscore functions, it goes like this:
# Theirs some behaviour that I want to implement on an object -> write some __ function __ (Data Model Methods)
# The pattern always goes like:
# Theirs some top-level function or top-level syntax and a corresponding __ function __
# E.g.

# The top level syntax invokes the double under score methods -> e.g. len() invokes __len__
# x + y     -> __add__ (top level syntax = "+" operator)
# init x    -> __init__
# repr(x)   -> __repr__
# len(x)    -> __len__
# x()       -> __call__


class Polynomial:
    def __init__(self, *coeffs):
        self.coeffs = coeffs

    def __repr__(self):
        """ Printable representation of this class -> This is called when I print(polynomial_object)"""
        return f'Polynomial({self.coeffs})'

    def __add__(self, other):
        """ This is called when I add polynomials (p1_object + p2_object) """
        return Polynomial(*(x + y for x, y in zip(self.coeffs, other.coeffs)))

    def __len__(self):
        """ Returns size of the polynomial in terms of its degree when we call len() on it """
        return len(self.coeffs)

    def __call__(self):
        """ We could implement this by calling something else """
        pass


# Notice __len__ implements the len() method on an object
# __add__ implements the "+" operator

# This is a pattern.
# Everytime we want to implement some custom behaviour on a python object,
# we do it by implementing a dunder method which ties to some top-level syntax ( e.g. __len__ ties to len() )
# And we implement on the object itself

p1 = Polynomial(1, 2, 3)  # x^2 + 2x + 3
p2 = Polynomial(3, 4, 3)  # 3x^2 + 4x + 3

# 3 CORE Patterns to really understand object oriented programming in python are:

# 1. The protocol view of python (The information above)
# 2. The built-in Inheritance protocol and how it works (Where you go on a python object to look for things)
# 3. Caveats on how OOP works in python