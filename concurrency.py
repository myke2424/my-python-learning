# --- Threads vs Async ---

# Threads switch pre-emptively (Time-slicing via the scheduler). This is convenient because you don't need to add explicit code to cause a task to switch.
# The cost of this convenience is that you have to assume a switch can happen at any time.
# Therefore critical sections of code have to be guarded with locks (Mutual Exclusion).
# The limit on threads = (Total CPU power - cost of tasks switches and synchronization overhead)
# The challenge of multi-threaded programs is finding out all the critical sections of code that require locks
# The whole reason for using threads is you have shared state, and if you have shared state, you have RACE CONDITIONS,
# you manage these race conditions through a lock, so when you want to modifiy the state, you acquire a lock, modify the state and then release the lock.

# Async switches cooperatively, so you don't get interrupted by the scheduler at arbitrary times.
# Instead, you add explicit code "yield" or "await" to cause a task to switch.
# The benefit of this is, since we control when task switches occur, generally we no longer need locks and other synchronization primitives.
# Also, the cost of task switches is very low. Async is very cheap.

# Since async cost is so low, it maximizes CPU utilization because it has less overhead than threads. Meaning it's faster.
# Easier to program since we don't require locks.
# The major CON of async is, it requires all code to be NON-BLOCKING.
# e.g. you can't just read a file synchronously or sleep anymore etc
# You need to load an event loop. switch all your calls to non-blocking calls and use async/await keywords.
# Async is much easier to get right than threads with locks, however threads require very little tooling (Really all you need is threads locks and queues)
# In an existing code base with no async, its easier to implement threading since you don't need to rewrite all your calls to non-blocking.
# "Fuzzing" is a good technique for debugging multi-threaded code by amplifying race-conditions.

# You can make threading more safe by utilizing queues.
# Sometimes you need global variables to communicate between functions, however in multi-threaded code, the mutable state is a problem.
# The better solution is to use threading.local() (a global within a thread)
# NEVER try to kill a thread from something external to that thread, if that thread you killed has a lock,
# this results in all the other threads waiting on the killed thread resulting in a dead lock.
# If you overuse locks, you're enforcing mutual exlcusion which is the opposite of parallel, which can lead to just sequential execution.
# Example of implementing a safe multi-threaded program using a message queue (we could use locks or queues to solve race conditions)

import threading, queue

counter_queue = queue.Queue()
counter = 0


# Other threads can't directly update the counter, they have to send a message to the counter manager to update it
# The queue updates it one at a time (FIFO)
# We want to increment and print sequentially, so we put the incrementing and printing in the same thread (Send message to printer queue)
def counter_manager():
    """ I and ONLY I, update the counter variable """
    global counter

    while True:
        increment = counter_queue.get()
        counter += increment
        print_queue.put(['The count is %d' % counter])
        counter_queue.task_done()


# Isolate the counter in its own daemon thread
t = threading.Thread(target=counter_manager)
t.daemon = True
t.start()
del t

print_queue = queue.Queue()


def print_manager():
    """ I and ONLY I, can call 'print' """
    while True:
        job = print_queue.get()
        for line in job:
            print(line)
        print_queue.task_done()


t = threading.Thread(target=print_manager)
t.daemon = True
t.start()
del t


def worker():
    """ My job is to increment the counte rand current count"""
    counter_queue.put(1)


worker_threads = []
for i in range(10):
    t = threading.Thread(target=worker)
    worker_threads.append(t)
    t.start()

# After the workers are done, use join()
for t in worker_threads:
    t.join()

counter_queue.join()
# Anytime we want to print, we send a message to our printer queue to print
print_queue(['Finishing Up'])
print_queue.join()
