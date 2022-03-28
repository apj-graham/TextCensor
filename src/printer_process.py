import time
from multiprocessing import Process

from src.safe_print import safe_print


class PrintThread(Process):
    def __init__(self, in_queue):
        super(PrintThread, self).__init__()
        self.in_queue = in_queue

    def run(self):
        while self.in_queue.empty():
            time.sleep(1)

        while True:
            print(self.in_queue.get(), end="")
            self.in_queue.task_done()
