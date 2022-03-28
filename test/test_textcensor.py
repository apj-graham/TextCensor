# -*- coding: utf-8 -*-
"""Test suite for TextCensor class"""

import io
import os
import sys
import unittest
import unittest.mock

sys.path.append("..")
from main import TextCensor


class TestTextCensor(unittest.TestCase):
    """Unit Tests for the TextCensor class"""

    BANNED_WORDS_FILE_PATH = os.path.abspath("test/test_resources/banned_words.txt")

    # def test_textcensor_accepts_valid_text_file(self):
    #    """A TextCensor instance can be created with a valid text file"""
    #    censor = TextCensor(self.BANNED_WORDS_FILE_PATH)
    #    self.assertEqual(self.BANNED_WORDS_FILE_PATH, censor.banned_words_filepath)
    #
    # def test_textcensor_rejects_non_existent_file(self):
    #    """An IOError is raised when a non existent file is used to create a TextCensor instance"""
    #    filepath = "non_existent_file.txt"
    #    with self.assertRaises(IOError):
    #        TextCensor(filepath)
    #
    # def test_textcensor_rejects_non_text_file(self):
    #    """An IOError is raised when a non text file is used to create a TextCensor instance"""
    #    filepath = "test_resources/non_text_file.png"
    #    with self.assertRaises(IOError):
    #        TextCensor(filepath)

    def test_banned_words_read_correctly(self):
        """Words are read correctly from the file provided"""
        control_words = ["fudge", "secret", "Mordor"]
        censor = TextCensor(self.BANNED_WORDS_FILE_PATH)
        test_words = list(censor.get_banned_words())

        # Check the correct number of words was read from the file
        self.assertEqual(len(control_words), len(test_words))

        for control, test in zip(control_words, test_words):
            self.assertEqual(control, test)

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_string_censored_correctly(self, mock_stdout):
        """A String has banned words replaced by an equal number of *'s"""
        plain_text = (
            "There are some words that one must not say such as fudge and secret"
        )
        # Print adds \n onto the end of returned string
        censored_text = (
            "There are some words that one must not say such as ***** and ******"
        )
        censor = TextCensor(self.BANNED_WORDS_FILE_PATH)

        censor.censor_line_and_print(plain_text)
        self.assertEqual(mock_stdout.getvalue(), censored_text)

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_text_censored_correctly(self, mock_stdout):
        """A text file has banned words replaced by an equal number of *'s"""
        text_filepath = os.path.abspath("test/test_resources/sample_text.txt")
        # Print adds a space onto the end of returned string
        censored_text = [
            "Three Rings for the Elven-kings under the sky,",
            "Seven for the Dwarf-lords in their halls of stone,",
            "Nine for Mortal Men doomed to die,",
            "One for the Dark Lord on his dark throne",
            "In the Land of ****** where the Shadows lie.",
            "One Ring to rule them all, One Ring to find them,",
            "One Ring to bring them all and in the darkness bind them",
            "In the Land of ****** where the Shadows lie.",
        ]
        censor = TextCensor(self.BANNED_WORDS_FILE_PATH)

        censor.censor_text(text_filepath)
        output_text = mock_stdout.getvalue().split("\n")
        for output_line, censored_line in zip(output_text, censored_text):
            self.assertEqual(output_line, censored_line)


if __name__ == "__main__":
    unittest.main()
