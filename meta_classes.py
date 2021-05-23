# Lets say this base class is from a 3rd party library (we can't change its implementation)

class Base:
    def foo(self):
        return 'foo'


# Since we depend on library code, we need checks in place to make sure the methods were implementing still exist.
# If the method doesn't exist, the code will fail and present the error message below
assert hasattr(Base, 'foo'), "Foo method doesnt exist"


# Doing this makes the Derived class enforce a constraint on the base class.
# It's saying the Base class needs these methods in order for the code to execute
class Derived(Base):
    def bar(self):
        return self.foo()


# Now lets flip the script and see how would we enforce the same but for the library code
# I need a way to enforce the user using this library implements a bar method, asserting like above won't work.
# Theirs two ways to solve this, the first way is a meta class.

# Meta classes are classes that derive from type
# They fundamentally allow you to intercept the construction of derived types

class BaseMeta(type):
    def __new__(cls, name, bases, body):
        # This gets called with our derived class
        print('BaseMeta.__new__', 'cls:', cls, 'name:', name, 'bases: ', bases, 'body:', body)
        # This is what it prints for the construction of our UserCode class

        # BaseMeta.__new__ cls: <class '__main__.BaseMeta'> name: UserCode bases:  (<class '__main__.LibraryCode'>,)
        # body: {'__module__': '__main__', '__qualname__': 'UserCode', 'bar': <function UserCode.bar at 0x7f9a31b33f70>}

        # You can see the "body" of the class shows all the methods implemented on our derived class
        # To validate the user implements the bar method, we can do the following:

        if 'bar' not in body:
            raise TypeError("User didn't implement bar method")

        return super().__new__(cls, name, bases, body)


class LibraryCode(metaclass=BaseMeta):
    def foo(self):
        return self.bar()


class UserCode(LibraryCode):
    def bar(self):
        return 'bar'


# So to be clear, we can use Metaclasses to enforce constraints on the construction of classes
# Typically useful to make sure a user who implements our library implements the required constraints

# Metaclasses can be clumsy, in python3.6 got the following new feature:

class NewBase():
    def foo(self):
        return self.bar()

    # This allows us to hook into when a subclass gets initialized
    def __init_subclass__(self, *args, **kwargs):
        print('init_subclass', a, kw)
        return super().__init__subclass__(*args, **kwargs)