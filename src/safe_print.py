from multiprocessing import Lock

lock = Lock()


def safe_print(*a, **b):
    lock.acquire()
    try:
        print(*a, **b)
    finally:
        lock.release()
