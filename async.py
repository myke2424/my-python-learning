import time
import asyncio
import random

# https://hynek.me/articles/waiting-in-asyncio/


#  --------- Asynchronous Code ---------

# Asyncio coroutines are the recommended building blocks of asyncio apps
# Coroutines can be described as functions that can be suspended/resumed (special kind of python generator)
# Coroutine functions are functions with an async prefix
# Calling a coroutine function, produces a coroutine object, that object needs to be scheduled
# Their are three main ways to schedule a coroutine object:

# Run it as the entrypoint to your app - e.g. asyncio.run(coroutine_object)
# We have to await coroutine objects
# This tells python to suspend the current coroutine until the sub-coroutine completes
# In this example, the sub-coroutine is asyncio.sleep

async def say_hello(num):
    sleep_duration = random.random()
    await asyncio.sleep(sleep_duration)
    print(f'num: {num}, sleep_duration: {sleep_duration}')


async def main():
    # Think of each method call as a task
    # Have to await it, because its an async function (coroutine)
    await say_hello(1)
    await say_hello(2)
    await say_hello(3)

    # To run these tasks concurrently we can trigger them all at the same time with asyncio.gather(coroutine_objs)
    await asyncio.gather(say_hello(1), say_hello(2), say_hello(3))

    # We can also schedule coroutines with asyncio.Task, a task is something we schedule to run in the future
    t1 = asyncio.create_task(say_hello(1))
    t2 = asyncio.create_task(say_hello(2))
    t3 = asyncio.create_task(say_hello(3))

    await t1
    await t2
    await t3


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print("Took", time.time() - start, "seconds")