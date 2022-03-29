"""The Process used to print the Censored text"""

import time
from multiprocessing import Process


class PrintProcess(Process):
    """Process that prints the Censored text.

    Takes censored words from the processed words queue as they arrive
    and prints them.

    The results can then be printed whilst other results are being procesed
    """

    def __init__(self, in_queue):
        super(PrintProcess, self).__init__()
        self.in_queue = in_queue

    def run(self):
        """Print censored words"""
        self._wait_until_words_available()

        while True:
            print(self.in_queue.get(), end="")
            self.in_queue.task_done()

    def _wait_until_words_available(self):
        """Wait until some words have been processed by the processing threads

        Continuously check to see if any words have been processed. If not, wait
        small while before trying again
        """
        while self.in_queue.empty():
            time.sleep(1)
