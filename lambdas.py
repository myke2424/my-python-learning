# Lambdas are just anonymous functions (e.g. js arrow function cb)
# Taken literally, an anonymous function is a function without a name.
# In Python, an anonymous function is created with the lambda keyword.

# We can apply the an argument to the lambda by surrounding the func and its arg with parentheses

(lambda x, y: x + y)(2, 3)  # this is immediately invoked and will return 5 (not recommended to do this)

add = lambda x, y: x + y

# Now we can call the lambda func
add(5, 5)


# This is the same as creating the function:
def add(x, y):
    return x + y


full_name = lambda first, last: print(f'Fullname: {first, last}')
full_name('Kobe', 'Bryant')

# Lambda functions are frequently used with higher-order-functions (a func that takes a func as a parameter or returns a function)

high_order_func = lambda x, func: func(x)

high_order_func(5, lambda x: x * 10)  # this will return 50

# You’ll use lambda functions together with Python higher-order (map, reduce, filter etc)

# Here's a quote from the python design history faq:
# Unlike lambda forms in other languages, where they add functionality, Python lambdas are only a shorthand notation if you’re too lazy to define a function


# A lambda function can’t contain any statements.
# In a lambda function, statements like return, pass, assert, or raise will raise a SyntaxError exception.
# Also, you can't use type annotations in a lambda (e.g. x: str)