# Lets create a function cached decorator then convert it into a class based decorator.
import functools


# Here's our cached function decorator, it will store the function argument and return value in the cache (dict)
def cachedd(func):
    cached_data = {}

    @functools.wraps(func)
    def cached_dec(*args):
        try:
            return cached_data[args]
        except KeyError:
            cached_data[args] = ret = func(*args)
            return ret

    return cached_dec


@cachedd
def compute(x: int) -> int:
    print(f'Calling with: {x}')
    return x * x


compute(5)  # First time it will call our side effect print statement and store the return val/args in the cache
compute(5)  # The print statement isnt executed, it retrieves the return value from the cache since it was called prior


# Now lets implement the same caching functionality but through a class decorator...
# We'll need to implement the __init__ and __call__ method

class cached:
    def __init__(self, func):
        self.func = func
        self.cached_data = {}

        # Class decorator way of forwarding __name__ etc.. to the decorated function (analagous to functools.wraps)
        # If we didn't do this, compute2.__name__ would raise an attribute error.
        functools.update_wrapper(self, func)

    def __call__(self, *args):
        try:
            return self.cached_data[args]
        except KeyError:
            self.cached_data[args] = ret = self.func(*args)
            return ret

    def __repr__(self):
        return repr(self.func)


@cached
def compute2(x: int, y: int) -> int:
    print(f'Computer 2 Calling with {x}, {y}')
    return x + y


# If we want to use decorator arguments, often referred to as a "Decorator factory pattern", we can do this
def cached_dec_with_args(maxsize: int):
    def cached_decorator(func):
        cached_data = {}

        @functools.wraps(func)
        def cached_dec(*args):
            try:
                return cached_data[args]
            except KeyError:
                if len(cached_data) == maxsize:
                    first_key = next(iter(cached_data))
                    print(f'Removing {first_key} from cache')
                    del cached_data[first_key]

                cached_data[args] = ret = func(*args)
                print(f'Updated cache: {cached_data}')
                return ret

        return cached_dec

    return cached_decorator


@cached_dec_with_args(maxsize=2)
def compute3(x: int) -> int:
    print(f'Compute3 calling with: {x}')
    return x * 2

