# Generator functions are a special kind of function that return a lazy iterator.
# You can loop over these objects, however, unlike iterators, they don't store their contents in memory

# A common use case of generator is to work with like data streams / files (CSV)

# Generator functions look and act just like regular functions, but with one defining characteristic.
# Generator functions use the Python yield keyword instead of return.


# This would most likely cause a memory error if the file is huge.
# A better way would be to use the generator alternative below.
def csv_reader_iterate(file_name):
    file = open(file_name)
    result = file.read().split("\n")
    return result


# This iterates through the rows in a file and yields a row
# This is a generator function (yield indicates this)
def csv_reader_generator(file_name):
    # Its also possible to define a generator expression (the generator version of list comprehension)
    for row in open(file_name, 'r'):
        # Using yield will result in a generator object.
        yield row


filename = 'data.csv'
# Its also possible to define a generator expression (the generator version of list comprehension)
# When you call a generator function or use a generator expression, you return a special iterator called a generator
csv_gen = (row for row in open(filename))


# You can define an infinite sequence generation with generators.
# Generating an infinite sequence requires the use of a generator since computer memory is finite

def infinite_sequence():
    num = 0
    while True:
        # yield indicates where a value is sent back to the caller
        # unlike return, you don't exit the function afterward (we can write code after the yield statement)
        yield num
        num += 1


for i in infinite_sequence():
    print(i, end=" ")

# Instead of using a for loop, you can also call next() on the generator object directly
# Were manually iterating over the object by calling next()
gen = infinite_sequence()
next(gen)  # prints 0
next(gen)  # prints 1
next(gen)  # prints 2

import sys

nums_squared_list = [i * 2 for i in range(10000)]
nums_squared_generator_object = (i ** 2 for i in range(10000))

# sys.getsizeof() shows the size of a python object in bytes
sys.getsizeof(nums_squared_list)  # 87,624 bytes
sys.getsizeof(nums_squared_generator_object)  # 120 bytes

# This means the list version is over 700 times larger than the generator object.

print()