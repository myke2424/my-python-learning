# Decorators provide a simple syntax for providing higher-order functions
# A higher order function takes a function as an argument or returns a pointer to a function (or both)
# In the end, a decorator is just a python function.

# Here's a simple example.
# We are "Decorating" the "function" that's being called
# Meaning, if we use this decorator on any function, it will print 'hello mike' before invoked.
def my_decorator(function):
    def hello():
        print('hello mike')
        function()

    return hello


def testing():
    print('Testing!!!')


test = my_decorator(testing)
test()


# Put simply: decorators wrap a function, modifying its behavior.
# The above way of writing a decorator is a little verbose.
# The short-hand version is the following:

@my_decorator
def testing_two():
    print('Testing again!')


testing_two()


# To create decorators more versatile, you can add *args and **kwargs to the inner wrapper function
# This will accept any number of arguments now
# The return value from the last execution of the function is returned
# Meaning this would return none, even if the function passed in had a return value
def do_twice(function):
    """ Calls the function twice """

    def wrapper_do_twice(*args, **kwargs):
        function(*args, **kwargs)
        function(*args, **kwargs)

    return wrapper_do_twice


@do_twice
def greet(name):
    print(f'Hello {name}')


# This will greet mike twice, because of the do_twice decorator
greet('mike')


# Now this will return a value
def do_twice_with_return(function):
    """ Calls the function twice """

    def wrapper_do_twice(*args, **kwargs):
        function(*args, **kwargs)
        return function(*args, **kwargs)

    return wrapper_do_twice


@do_twice_with_return
def get_name(name):
    print(f'{name}')
    return f'Name is {name}'


get_name('michael')

# ------------- Real World Examples  -------------

import functools


# This formula is a good boilerplate template for building more complex decorators
def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value

    return wrapper_decorator


# The following @debug decorator will print the arguments a function is called with as well as its return value
# every time the function is called

def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1 Create a list of positional args
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2 Create a list of kew word args
        signature = ", ".join(args_repr + kwargs_repr)  # 3 # Create a list of all args (join args and kwargs)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4 Print the return value of the function
        return value

    return wrapper_debug


@debug
def add(x, y):
    return x + y


# The debug decorator will output:
# Calling add(5, 5)
# 'add' returned 10
add(5, 5)

import time


# Maybe you want to sleep before a function is called
def slow_down(func):
    """Sleep 1 second before calling the function"""

    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper_slow_down


@slow_down
def countdown(from_number):
    if from_number < 1:
        print("Liftoff!")
    else:
        print(from_number)
        countdown(from_number - 1)


countdown(3)

# Is the User Logged In?
# In this example, we are using Flask to set up a /secret web page that should only be visible to users that are logged in or otherwise authenticated:

# def login_required(func):
#     """Make sure user is logged in before proceeding"""
#     @functools.wraps(func)
#     def wrapper_login_required(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for("login", next=request.url))
#         return func(*args, **kwargs)
#
#     return wrapper_login_required
#
#
# @app.route("/secret")
# @login_required
# def secret():
#     pass


import logging
import sys

logger = logging.getLogger(__name__)


def exception_handler(exception, err_msg=None, verbosity=False):
    """ Wraps the decorated function with a try except using the exception arg """

    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except exception as e:
                if err_msg is not None:
                    logger.error(err_msg)
                else:
                    logger.error(e)

                if verbosity is True:
                    type_, value, traceback = sys.exc_info()

                    logger.debug(f'Exception Type {type_}')
                    logger.debug(f'Exception Instance: {value}')
                    logger.debug(f'Traceback: {traceback}')

        return inner

    return wrapper


@exception_handler(exception=TypeError, err_msg='Cant add a string with an int...', verbosity=True)
def add(x, y):
    z = x + y
    return z


add(5, "5")