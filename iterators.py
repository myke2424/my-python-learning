# Objects that support __iter__ and __next__ dunder methods automatically work with for-in loops
# https://dbader.org/blog/python-iterators
# Defining this will allow our for-in iteration to work
class RepeaterIterator:
    def __init__(self, source):
        self.source = source

    def __next__(self):
        return self.source.value


# The repeater class will repeatedly return a single value when iterated over
class Repeater:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return RepeaterIterator(self)


# The two dunder methods we defined, __iter__ and __next__, are the key to make a python object iterable

repeater = Repeater('mike')

for item in repeater:
    print(item)

# Behind the scenes of this for loop, it looks like:
iterator = repeater.__iter__()
while True:
    item = iterator.__next__()
    print(item)

# It first prepared the repeater object for iteration by calling its __iter__ method. This returned the actual iterator object.
# After that, the loop repeatedly calls the iterator object’s __next__ method to retrieve values from it.

# This has the same behaviour as above. Internally these methods invoke the __iter__ and __next__ dunder methods.
iterator = iter(repeator)
next(iterator)


# All that matters is that __iter__ returns any object with a __next__ method on it.
# A simply way of expressing aboves classes is the following:

class Repeat:
    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

    def __next__(self):
        return self.value


# Now lets actually define an iterator that isn't an infinite loop.
# Iterators use exceptions to structure control flow.
# To signal the end of iteration, a Python iterator simply raises the built-in StopIteration exception.
# Iterators can't be reset, you'll need to initialise a new interator object

class BoundedRepeater:
    def __init__(self, value, max_repeats):
        self.value = value
        self.max_repeats = max_repeats
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_repeats:
            raise StopIteration
        self.count += 1
        return self.value


# This gives us the desired result. Iteration stops after the number of repetitions defined in the max_repeats parameter:

bounded_repeater = BoundedRepeater('Mike', 3)
for item in bounded_repeater:
    print(item)  # This only prints 3 times

# This is the same as writing
while True:
    try:
        item = next(iterator)
    except StopIteration:
        break
    print(item)

# Every time next() is called in this loop we check for a StopIteration exception and break the while loop if necessary.:w:wq
