# Retaining State with Inner functions: CLOSURE!
# In python you can create higher-order-functions since functions are first class citizens

# Retaining state in a Closure
# A closure causes the inner function to retain the state of its environment when called, e.g.
# This way, when you call the instance of power returned by generate_power, it remembers the value of exponent

def generate_power(exponent):
    def power(base):
        return base ** exponent

    return power


p = generate_power(4)
p(2)  # returns 4 ** 2 (It uses the exponent from the first call)
print(p(2))  # 16

