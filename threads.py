# When it comes to threading, we're going to see a lot of benefit when our tasks are I/O bound.
# When we are waiting around for a lot Input/Output operations such as reading from disk or network operations, that's where threading thrives.
# If our tasks are CPU bound, we won't see much benefit from using threading, it could even result in a slower program due to the overhead from threads.
# For CPU bound tasks we should use multi-processing and run the tasks in parallel instead.

import threading
import time

start = time.perf_counter()


def do_something(seconds):
    print(f'Sleeping {seconds} seconds')
    time.sleep(seconds)
    print('done sleeping...')
    return 1


# Create the threads by giving it a target function and the args the function receives, in this case its 1 argument (seconds)
t1 = threading.Thread(target=do_something, args=[1])
t2 = threading.Thread(target=do_something, args=[1])

# Start the threads
t1.start()
t2.start()

# Make sure the threads complete before calculating the finish time
t1.join()
t2.join()

finish = time.perf_counter()
print(f'Finished in {round(finish - start, 2)} second(s) ')

# Loop example
# We can't thread.join() in the loop because it would join the thread each iteration resulting in synchronous code
start_loop = time.perf_counter()
threads = []

for _ in range(10):
    t = threading.Thread(target=do_something, args=[1])
    t.start()
    threads.append(t)

for t in threads:
    t.join()

finish_loop = time.perf_counter()
print(f'Finished in {round(finish_loop - start_loop, 2)} second(s) ')

# An easier and more efficient way to run threads in python is to use the ThreadPool Executor

import concurrent.futures

# If we want to execute the function once a time, use submit()
# Submit schedules a function to be executed and returns a future obj
# A future object encapsulates function execution and allows us to poll it once its been scheduled
# submit() takes the function and its args
with concurrent.futures.ThreadPoolExecutor() as executor:
    seconds = [5, 4, 3, 2, 1]
    # map returns the results in the order they started. Uses a new thread for each call
    results = executor.map(do_something, seconds)
    for result in results:
        print(result)

    results = [executor.submit(do_something, second) for second in seconds]

    # iterator that will yield the results of our threads as they are completed
    for f in concurrent.futures.as_completed(results):
        print(f.result())

# Example downloading images concurrently using the thread pool executor

import requests

img_urls = [
    'https://images.unsplash.com/photo-1516117172878-fd2c41f4a759',
    'https://images.unsplash.com/photo-1532009324734-20a7a5813719',
    'https://images.unsplash.com/photo-1524429656589-6633a470097c',
]

t1 = time.perf_counter()


def download_image(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[3]
    img_name = f'{img_name}.jpg'
    with open(img_name, 'wb') as img_file:
        img_file.write(img_bytes)
        print(f'{img_name} was downloaded...')


# This is a good use-case for multi-threading since downloading and writing to the file are I/O bound tasks,
# If we were doing processing on these images, that would be CPU bound which is where multi-processing will be ideal.
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_image, img_urls)

t2 = time.perf_counter()

print(f'Finished in {t2 - t1} seconds')
