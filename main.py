# -*- coding: utf-8 -*-
"""A Script to censor a given text file by replacing given words with *'s"""
import os
import string
import time
from multiprocessing import JoinableQueue, Value

from src.arg_parser import parse_arguments
from src.censor_process import CensorProcess
from src.input_validation import validate_arguments
from src.printer_process import PrintProcess


class TextCensor:
    """
    A class to encapsulate functionality needed to censor a text file.

    Makes uses of multiprocessing to censor multiple words in parallel.
    This provides a performance inprovement when the list of banned words
    is very long.

    Words in the text to be censored are numbered to ensure they are printed
    in the same order they are read in.

    ...

    Attributes
    ----------
    banned_words_filepath: str
        The filepath of the .txt document containing the words to be censored

    Methods
    -------
    censor_text(text_filepath):
        Replaces censor words in text with *'s

    censor_line_and_print(line):
        Replaces censor words in given string with *'s and prints the result

    get_banned_words():
        Return the banned words in the banned words file
    """

    # Longest word in the disctionary. We do not expect to see any longer words in the text
    MAX_BUFFER_SIZE = 45

    # ' can be part of a word so we remove it. We also assume words aren't split across lines
    WORD_END_CHARACTERS = string.punctuation.replace("'", "") + " \n"

    def __init__(self, banned_words_filepath):
        """
        Constructs all the necessary attributes for the TextCensor object

        Parameters
        ----------
        banned_words_filepath : str
            filepath of the text file containing the words to be censored
        """

        self.banned_words_filepath = banned_words_filepath

        self.read_words = JoinableQueue()
        self.proccessed_words = JoinableQueue()
        self.read_words_count = 0
        self.processed_words_count = Value("l", 0, lock=True)
        self.processes = []

        self.char_buffer = []
        self.end_of_file = False

    def initialise_processes(self):
        """Initialises the processes used to censor each word of text as well as the
        proccess that is used to print the results of censoring each word.

        Will only create processes equal to the number of cpu cores - 1

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for _ in range(os.cpu_count() - 2):
            process = CensorProcess(
                self.read_words,
                self.proccessed_words,
                self.banned_words_filepath,
                self.processed_words_count,
            )
            process.daemon = True
            process.start()
            self.processes.append(process)

        process = PrintProcess(self.proccessed_words)
        process.start()
        self.processes.append(process)

    def censor_text(self, text_filepath):
        """
        Reads text in from file, sensors it and then prints the resultant text

        Parameters
        ----------
        text_filepath : str
            The file path of the file containing the text to be censored

        Returns
        -------
        None
        """
        self.initialise_processes()

        with open(text_filepath, "r", encoding="utf-8") as text:
            buffer = []

            while not self.end_of_file:
                if len(buffer) >= self.MAX_BUFFER_SIZE:
                    # Reset buffer as we are sure whatever is in the buffer is not a word
                    buffer = []

                char = text.read(1)
                if char:
                    buffer += char
                    if char in self.WORD_END_CHARACTERS:
                        self.add_word_to_queue(buffer)
                        buffer = []
                else:
                    # We have reached the end of the file
                    self.add_word_to_queue(buffer)
                    self.end_of_file = True
                    buffer = []

        self.read_words.put(("\n", self.read_words_count + 1))
        self.read_words.join()
        time.sleep(1)
        self.proccessed_words.join()

        for process in self.processes:
            process.kill()

    def add_word_to_queue(self, buffer):
        """Add word to queue of words to be processed and update the number of
        words that have been read from the file.

        Arguments:
            buffer: list
                list of characters that form a word
        """
        self.read_words_count += 1
        self.read_words.put(("".join(buffer), self.read_words_count))


if __name__ == "__main__":
    args = parse_arguments()
    validate_arguments(args.banned_words_file, args.document)

    start_time = time.time()
    censor = TextCensor(args.banned_words_file)
    censor.censor_text(args.document)
