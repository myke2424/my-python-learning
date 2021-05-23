# The factory pattern is a creational pattern that defines an interface for creating an object and defers instantiation until runtime
# Used when you don't know how many or what type of objects will be needed until during run time

# Chair Factory Example


# imports are used to enforce the rules of the interface
# Interface doesnt have any method bodies

class IChairInterface:
    @staticmethod
    def get_dimensions():
        pass


# Create some Concrete classes that implement the IChairInterface

class BigChair(IChairInterface):
    def __init__(self):
        self.height = 80
        self.width = 80
        self.depth = 80

    def get_dimensions(self):
        return {"height": self.height, "width": self.width, "depth": self.depth}


class MediumChair(IChairInterface):
    def __init__(self):
        self.height = 60
        self.width = 60
        self.depth = 60

    def get_dimensions(self):
        return {"height": self.height, "width": self.width, "depth": self.depth}


class SmallChair(IChairInterface):
    def __init__(self):
        self.height = 20
        self.width = 20
        self.depth = 20

    def get_dimensions(self):
        return {"height": self.height, "width": self.width, "depth": self.depth}


# Create the Factory -> Creates different chair objects

class ChairFactory():
    @staticmethod
    def get_chair(chair_type):
        try:
            if chair_type == 'BigChair':
                return BigChair()
            elif chair_type == 'MediumChair':
                return MediumChair()
            elif chair_type == 'SmallChair':
                return SmallChair()
            else:
                raise ValueError('Chair Not Found')
        except ValueError as e:
            print(e)


# Factory.py (this file) is the client, it asks the ChairFactory to get a chair and the factory returns
# a concrete implementation of a chair object depending on the chair type
# Each concrete implementation implements the IchairInterface

if __name__ == "__main__":
    chair = ChairFactory.get_chair("BigChair")
    chair2 = ChairFactory.get_chair("MediumChair")
    chair3 = ChairFactory.get_chair("SmallChair")
    print(chair.get_dimensions())
    print(chair2.get_dimensions())
    print(chair3.get_dimensions())