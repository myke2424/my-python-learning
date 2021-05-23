# Context managers are fundamentally a way to include a setup and teardown action to some logic

# The reason we use a context manager here, is because it includes the setup / teardown.
# For setup it opens the file, and for teardown it closes the file

with open('dunders.py') as f:
    pass

from sqlite3 import connect

# The setup and teardown of this is opening and close the DB connection
with connect('test.db') as conn:
    cur = conn.cursor()

# with ctrx() as x:
#   pass

# This is top-level syntax, behind the scenes it actually looks like:
x = ctrx().__enter__()
try:
    pass
finally:
    x.__exit__()


# This is how we implement our own context manager, we implement the enter and exit dunder methods
# Lets create our own context manager that creates a db table for setup and drops it for teardown

class temptable:
    def __init__(self, cur):
        self.cur = cur

    def __enter__(self):
        self.cur.execute('create table points(x int, y int)')

    def __exit(self, *args):
        self.cur.execute('drop table points')


with connect('test.db') as conn:
    cur = conn.cursor()
    with temptable(cur):
        pass
    # The context manager will create our temp table and drop it when its done
    # Execute some SQL