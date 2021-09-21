import multiprocessing
import time

start = time.perf_counter()


def do_something(seconds):
    print(f'Sleeping {seconds} seconds')
    time.sleep(seconds)
    print('done sleeping...')
    return 1


def main():
    # Similar to threads, give the process a function and its args
    # Processes take a little longer to spin up vs threads
    # Arguments must be able to be serialized with pickle
    p1 = multiprocessing.Process(target=do_something, args=[3])
    p2 = multiprocessing.Process(target=do_something, args=[3])

    # Start the processes
    p1.start()
    p2.start()

    # join() will ensure the process will finish before moving on in the script
    p1.join()
    p2.join()

    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s) ')

    start_loop = time.perf_counter()
    processes = []

    for _ in range(10):
        p = multiprocessing.Process(target=do_something, args=[1])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    end_loop = time.perf_counter()
    print(f'Finished in {round(end_loop - start_loop, 2)} second(s) ')

    # An easier to way to implement multi-processing is using the process pool executor (similar to threadpool)
    import concurrent.futures

    # map returns the results in the order the processes were started
    # If the function raises an exception, the exception will be raised when you grab the result from the results iterator
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(do_something, [1, 2, 3, 4, 5])

        for result in results:
            print(result)


if __name__ == "__main__":
    main()
