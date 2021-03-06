""" Process that censors individual words"""

import re
import time
from multiprocessing import Process


class CensorProcess(Process):
    """Process the censors anyword on the banned words list

    With multiple processes, many words can be censored in parallel

    Arguments:
        in_queue : Queue
            FIFO buffer where words to be censored are collected from

        out_queue: Queue
            FIFO buffer where words that have been censored at put to

        banned_words_filepath: str
            Location of file containing the words to be censored

        counter: Value
            Variable shared between processes to keep track of which words
            have already been processed
    """

    # We only want to match a full word not words within words
    # e.g. "thought" contains "ought". We don't want to return
    # th***** if the banned word is ought

    # Also, test words are provided with the trailing character
    # (one of space, carriage return or punctuation)
    PATTERN_TEMPLATE = r"(?<!.)({})(?=\W)"

    def __init__(self, in_queue, out_queue, banned_words_filepath, counter):
        super(CensorProcess, self).__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.banned_words_filepath = banned_words_filepath
        self.processed_words_counter = counter

    def run(self):
        """Continously check for new words and sensor any that are available"""
        while True:
            word, word_number = self.in_queue.get()
            censored_text = self.process(word)
            while not self.processed_words_counter.value == word_number - 1:
                # Add sleep to avoid unneccesarily busy loop
                time.sleep(0.1)

            with self.processed_words_counter.get_lock():
                self.out_queue.put(censored_text)
                self.in_queue.task_done()
                self.processed_words_counter.value += 1

    def process(self, text):
        """
        Replace banned words in the given text with an equivalent number of *'s. Print
        result to stdout

        Parameters
        ----------
        text : str
            The string to be censored

        Returns
        -------
        None
        """
        for word in self.get_banned_words():
            pattern = self.PATTERN_TEMPLATE.format(word)
            stars = "".join(["*" for _ in word])
            censored_text = re.sub(pattern, stars, text, flags=re.IGNORECASE)
            if text != censored_text:
                # If we have already found the given word matches a banned word we break
                # to avoid having to search all the remaning words
                break
        return censored_text

    def get_banned_words(self):
        """
        Generator to read banned _words file and return each word in turn.

        It is assumed each word to be censored is on a new line

        Parameters
        ----------
        None

        Returns
        -------
        word : str
            One of the words to be censored in the text
        """
        with open(self.banned_words_filepath, "r", encoding="utf-8") as banned_words:
            for line in banned_words:
                # Remove whitespace so we aren't searching for that too
                word = line.strip()
                yield word
