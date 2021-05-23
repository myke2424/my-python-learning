# Under the hood, a hash table uses a DYNAMIC ARRAY of LINKED LISTS to
# efficiently store key/value pairs

# When instering a key/value pair, a hash function first maps the key which
# is typically a string to an integer value. This integer value represents an
# index in the underlying dynamic array.

# Then, the value associated with the key is added to the linked list stored at
# that index in the dyanmic array, and a reference to the key is also stored
# with the value.

# The following are a hash table's standard operations:

# - Inserting a key/value pair: O(1)
# - Removing a key/value pair: O(1)
# - Looking up a key: O(1)

# The worst case linear time operations occur when a hash table experiences a
# lot of collisions, leading to long lists interally, which take O(N) to
# traverse.

# Below is an example of what a hash table might look like under the hood:

# [
#   0: (val1, key1) -> null
#   1: (val2, key2) -> (val3, key3) -> (val4, key4)
#   2: (val5, key5) -> null
# ]

# In this example: key2,key3 and key4 collided by all being hashed to the same
# index 1. So to know which key is the correct one, it would need to traverse
# the linked list at this index.

# But how can we figure out which index we should store a value in by a string
# key?

# To do this, we need to know the size of the underlying array. We can generate
# a number representation (hash function) of our string and then using the modulus operate, we
# can mod the number by the length of the underlying array.
# That would then give us a index position that our value should be stored in.

# The important part is that this code is repeatable and we get the same index
# integer over and over again if the same key is being hashed.

# Remember, modulo returns the remainder after division
# E.g. 3030 % 12 = 3030 / 12 = 252.5 = .5 * 12 = 6


# This will always return an index that exist within our array.
# An example of this would be the follow implementation:
def get_index(key: str, arr_length: int):
    return hash(key) % arr_length


# To handle collisions in our hash table class, we will store a list of key value pairs for each index
# E.g. ("Key", "Value")

# arr = [ [("foo", "value"), ("bar", "value2")], [("hello", "value3"), ("world", "value4")] ]

# For this example, instead of storing each index as a linked list, we will
# store each index as an array.


class HashTable:
    def __init__(self, length):
        self.array = [None] * length

    def hash(self, key: str):
        """ Return the index in our underlying array for the given key """
        return hash(key) % len(self.array)

    def __repr__(self):
        return str(self.array)

    def add(self, key, value):
        """ Add a value to our array by its key """
        index = self.hash(key)

        if self.array[index] is not None:
            # This index contains some values.
            # We need to check if the key we're adding already exists, this
            # way, we can update it with the new value, this way, we can update
            # it with the new value

            # kvp = key/value pair
            for kvp in self.array[index]:
                # If the key is found, then update the current value to the new
                # value.

                if kvp[0] == key:
                    kvp[1] = value
                    break

            # Remember for/else, the else executes after the loop completetes
            # normally. Meaning, if no breaks happen, it will execute this else
            # statement.
            else:
                # If no breaks happened, it means that no existing key was
                # found. Therefore, we can simply append it to the end of the
                # list at this index.
                self.array[index].append([key, value])

        else:
            # This index is empty. We will create an empty list and append the
            # key value pair.
            self.array[index] = []
            self.array[index].append([key, value])

    def get(self, key: str):
        """ Returns a value by its key, return None if the key isnt found """

        index = self.hash(key)

        if self.array[index] is None:
            return None
        else:
            # Loop through all the key/value pairs at this index, and find if
            # our key exists. If it does, return the value.

            for kvp in self.array[index]:
                if kvp[0] == key:
                    return kvp[1]

        return None


# With this implementation, if we have alot of collisions of indexes, it means
# adding/searching for a key will be worst case O(N) time.

# To improve on this, we want to reduce the amount of collisions
# So, with our current implementation, let's say we have a hash table
# initialized with a length of 4.

# This means, when we add our second key/value pair, theirs a 25% chance we
# have a collision.
# Soon all indexes get populated and then we have a linear time lookup as we're
# looping through east list of values

# To fix this, we need to implement array resizing to keep the size of the list
# flexible. We allow it to expand whenever it determines that its too
# populated.

# Meaning, we can always guarentee that the risk of collision is below a
# certain threshold.

# Here's the implementation adding the resizing methods.


class HashTableWithResizing:
    def __init__(self, length):
        self.array = [None] * length

    def __repr__(self):
        return str(self.array)

    def hash(self, key):
        return hash(key) % len(self.array)

    def is_full(self):
        """ Determines if the hash table is too populated """
        items = 0

        # Count the indexes
        for item in self.array:
            if item is not None:
                items += 1

        # Return bool based on if amount of items are more than half the length
        # of the list.
        return items > len(self.array) / 2

    def double(self):
        """ Doubles the list length and dumps the old array values into the new one """
        new_array_len = len(self.array) * 2
        new_hash_table = HashTableWithResizing(new_array_len)

        for i in range(len(self.array)):
            if self.array[i] is None:
                continue

            for kvp in self.array[i]:
                """ Dump our old values into the new hash table with the add method """
                new_hash_table.add(kvp[0], kvp[1])

        self.array = new_hash_table.array

    def add(self, key, value):
        index = self.hash(key)

        if self.array[index] is not None:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    kvp[1] = value
                    break
            else:
                self.array[index].append([key, value])
        else:
            self.array[index] = []
            self.array[index].append([key, value])

        # Double our array size if it's full after adding a key/val pair
        if self.is_full():
            self.double()

    def get(self, key):
        index = self.hash(key)

        if self.array[index] is None:
            return None
        else:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    return kvp[1]

        return None


# So now we're resizing our underlying array any time it hits the threshold.
# Therefore reducing collisions
