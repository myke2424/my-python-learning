import os

# HOW TO IMPLEMENT DEPENDENCY INJECTION???

# Easy. Objects do not create each other anymore.
# They provide a way to inject the dependencies instead.
# E.g. Taking them as a parameter

# Here's a bad example where we create objects inside a method.
# We can make this more flexible with dependency injection.


class ApiClient:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')  # <-- Dependency
        self.timeout = os.getenv('TIMEOUT')  # <-- Dependency


class Service:
    def __init__(self):
        self.api_client = ApiClient()  # <-- Dependency


def main():
    service = Service()  # <-- Dependency


class ApiClientDI:
    """ This class implements dependency injection """
    def __init__(self, api_key, timeout):
        self.api_key = api_key  # <-- Dependency is injected
        self.timeout = timeout  # <-- Depedency is injected


class ServiceDI:
    """ This class implements dpendency injection """
    def __init__(self, api_client):
        self.api_client = api_client  # <-- Dependency is injected


def main_di(service):
    pass


if __name__ == '__main__':
    api_client = ApiClientDI(api_key=os.getenv('API_KEY'),
                             timeout=os.getenv('timeout'))
    main(Service(api_client))

# ApiClientDI is decoupled from knowing where the parameters come from.
# This makes things flexible. We have options and aren't constrainted to only
# getting the API KEY from as an env variable.
# We could store the key in the DB, use a yml config file etc. This makes it
# easy to change if needed and unit test our code

# Service is the same, it's decoupled from the api client. It does not create
# it anymore.

# However, flexibility comes with a price.
# Now you need to assemble and inject objects
# E.g. creating an api client object based off a config yml file and passing it
# to the main function.

# Dependency Injection brings 3 advantages.

# 1. Flexibility: Components are loosely coupled. You can easily extend or
# change a fuctionality. E.g. changing a DB and passing the object around

# 2. Testabilty: Testing is easier because you can easily inject mocks instead
# of real objects that use API connections.

# 3. Clearness and maintainabilty: Dependency Injection helps you reveal the
# dependencies. Implicit becomes explicit. And "Explicit" is better than
# implicit.

# The advantages of dependency injection really shine when trying to build a
# big application. The larger the app, the more significant the benefit.