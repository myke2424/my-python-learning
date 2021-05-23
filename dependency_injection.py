# Dependency Injection Notes!
# Dependency definition: A uses B methods, A has a dependency on B

# Inversion of Control:
# Objects do not create other objects on which they rely to do their work.
# Instead, they get the objects that they need from an outside source.
# E.g. A YML Configuration File

# Example of normal flow of control:
# A user has a database attribute, which he uses to call and persist data.


class User:
    def __init__(self):
        self.database = Database()


# Now we can invert the flow of control (Inversion Of Control)
# The relationship role between the dependencies should be REVERSED.
# Meaning, instead of the user instantiating the DB object,
# The DB object would be created elsewhere and passed to the user as paramter.
# Therefore we relinquish all responsibility of the DB object and somebody just
# hands it to us.
# That allows us to depend on more abstractions rather than concrete
# implentations.
# This promotes loosely coupled architecture, flexibilty, pluginability with
# our code.

# Depenency Injection generally means passing a dependent object as a parameter
# to a method, rather than having the method create the depedent object.
# What it means in practice is that the method does not have a direct depenency
# on a particular implementation; any implementation that meets the
# requirements can be passed in as a parameter.

# Typically instead of relying on the hard-coded implementations like;
# MySQL, Oracle, MongoDB etc.
# Instead we rely on more abstract implementations such as a database interface

# === BAD EXAMPLE SHOWING HARDCODED CONCRETE IMPLEMENTATION ===
# This bad, we're relying on a concrete implementation of a DB.
# This will be hard to swap DBs in the future.
# Also, this will be really hard to unit test because we rely soley on a,
# MySQL instance. We can't pass in a mock instance of a DB.


class User:
    def __init__(self):
        self.mysql_db = MySqlDb()

    def add(self, data):
        self.mysql_db.persist(data)
        print(f'Persisting data {data} to mysql db')


class MySqlDb():
    pass


# We can flip the inversion of control and pass the db in as a param
# This is dependency injection, we are passing depedencies down the control
# graph.


class UserIoC:
    def __init__(self, database):
        self.database = database

    def add(self, data):
        self.database.persist(data)
        print(f'Persisting data {data} to database')


# Instead of creating/handling the lifecycle of the DB Object,
# We can let somebody else do that for us, and take it as a parameter to our
# method.

# RELY ON ABSTRACTIONS RATHER THAN CONCRETE IMPLEMENTATIONS!
# In a statically typed language, we would create a Database interface and only
# objects that implement that interface, can be used as the DB passed to the
# user.

# Example:

from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def persist(data):
        pass


class Mysql_DB(DatabaseInterface):
    def persist(data):
        pass


class UserIoc:
    def __init__(self, db: 'DatabaseInterface'):
        self.db = db

    def add(self, data):
        self.db.persist(data)


# Now we can have whatever database we want. We have loosely coupled reliance
# on the type of DB. We have plugability.

# A dependency injection container would be analogous to a YML FILE.
# We create depedencies in a yml config file, and inject them into the code
# E.g. creating user objects based on yml config