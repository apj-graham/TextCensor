# -*- coding: utf-8 -*-
"""A Script to censor a given text file by replacing given words with *'s"""

import re
import copy
import os
import magic



class TextCensor():
    """
    A class to encapsulate functionality needed to censor a text file

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

    # We only want to replace full words so we include \b either side of the search word
    PATTERN_TEMPLATE = "\\b({})\\b"

    def __init__(self, banned_words_filepath):
        """
        Constructs all the necessary attributes for the TextCensor object

        Parameters
        ----------
        banned_words_filepath : str
            filepath of the text file containing the words to be censored
        """
        self.banned_words_filepath = banned_words_filepath

        self.validate_filepath(self.banned_words_filepath)

    def print_censor_text(self, text_filepath):
        """
        Prints the censored version of the text in the given text file to stdout

        Parameters
        ----------
        text_filepath : str
            The file path of the file containing the text to be censored

        Returns
        -------
        None
        """
        self.validate_filepath(text_filepath)
        with open(text_filepath, "r",encoding="utf-8") as text:
            for line in text:
                self.censor_line_and_print(line)

    def censor_line_and_print(self, text):
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
        censored_text = copy.deepcopy(text)
        for word in self.get_banned_words():
            pattern = self.PATTERN_TEMPLATE.format(word)
            stars = "".join(["*" for _ in word])
            censored_text = re.sub(pattern, stars, censored_text, flags=re.IGNORECASE)
        print(censored_text)

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

    @staticmethod
    def validate_filepath(filepath):
        """
        Checks the given filepath exists and that the file at that path is a text file

        Parameters
        ----------
        filepath : str
            The file path to be validated

        Returns
        -------
        None

        Raises
        ------
        IOError
        """
        # Check filepath exists
        if not os.path.exists(filepath):
            raise IOError(f"{filepath} does not exist.")

        # Check file given is a text file
        file_type = magic.from_file(filepath, mime=True)
        if file_type != 'text/plain':
            raise IOError(f"File provided is not a text file. File given was a {file_type} file")



if __name__ == "__main__":
    censor = TextCensor("banned_words.txt")
    censor.censor_text("enwik9.txt")
