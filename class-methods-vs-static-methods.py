# Class methods are methods which only using class properties, NOT INSTANCE PROPERTIES (defined in __init__)
# Static methods use no class or instance properties (they're independent functions grouped under a class)


class FTP:
    port = 21

    def __init__(self):
        pass

    @classmethod
    def transfer(cls, server_ip, files):
        # The cls parameter replaces the self parameter in a class method
        print(f'Using FTP port {cls.port}')
        print(f'Transfering {files} to {server_ip}')

    @staticmethod
    def help():
        print(
            'The File Transfer Protocol is a standard network protocol used for the transfer of computer files'
        )


# Invoke the class method
FTP.transfer('172.42.51.128', ['app.js', 'package.json'])

# Invoke the static method
FTP.help()

# A good use-case for class methods, is to use the class method as a second
# constructor. E.g.


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_input(cls):
        """ Second constructor to create a person object based on user input """

        name = input('Enter your name')
        age = input('Enter your age')

        return cls(name=name, age=age)