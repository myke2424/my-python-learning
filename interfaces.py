# Informal Way of implmenting an Interface
# This way won't error out if you dont implement all the interfaces methods

class InformalUserInterface:
    # This is an abstract method, describing the method with no logic
    def create_post(self, post: str) -> str:
        pass


class User(InformalUserInterface):
    """Over load methods to implement interface"""

    def create_post(self, post: str) -> str:
        return f'Post: {post}'


# Use Metaclasses to implement interfaces
# so it will error out if you dont define all the interface methods and call (issubclass)
# remember that `type` is actually a class like `str` and `int` so you can inherit from it
class UserMeta(type):
    """ A User Meta Class that will be used for User Class Creation """

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return hasattr(subclass, 'create_post') and callable(subclass.create_post)


# python3 metaclass sytnax: metaclass=
class UpdatedInformalUserInterface(metaclass=UserMeta):
    """" This interface is used for concrete classes to inherit from.
    There is no need to define the UserMeta methods as any class
    as they are implicitly made available via .__subclasscheck__(). """
    pass


class UserNew:
    def __init__(self):
        self.name = 'mike'

    def create_post(self, post: str) -> str:
        return f'{self.name} : {post}'


# Check if UserNew implements the interface -> Will return false if it doesnt have the methods in the interface
print(issubclass(UserNew, UpdatedInformalUserInterface))

user = UserNew
user.age = 24
u = user()

# Create a class with type
# the function type is in fact a metaclass.
# type is the metaclass Python uses to create all classes behind the scenes.
ClassCreatedFromType = type('ClassCreatedFromType', (), {"lang": "python"})

c = ClassCreatedFromType()
print(c.lang)


# Metaclasses are the 'stuff' that creates classes.
# Well, metaclasses are what create these objects
# You can call them a 'class factory'