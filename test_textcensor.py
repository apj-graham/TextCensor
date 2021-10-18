# -*- coding: utf-8 -*-
"""Test suite for TextCensor class"""


import unittest
import unittest.mock
import io
from sensor_text import TextCensor


class TestTextCensor(unittest.TestCase):
    """Unit Tests for the TextCensor class"""

    def test_textcensor_accepts_valid_text_file(self):
        """A TextCensor instance can be created with a valid text file"""
        filepath = "banned_words.txt"
        censor = TextCensor(filepath)
        self.assertEqual(filepath, censor.banned_words_filepath)

    def test_textcensor_rejects_non_existent_file(self):
        """An IOError is raised when a non existent file is used to create a TextCensor instance"""
        filepath = "non_existent_file.txt"
        with self.assertRaises(IOError):
            TextCensor(filepath)

    def test_textcensor_rejects_non_text_file(self):
        """An IOError is raised when a non text file is used to create a TextCensor instance"""
        filepath = "non_text_file.png"
        with self.assertRaises(IOError):
            TextCensor(filepath)

    def test_banned_words_read_correctly(self):
        """Words are read correctly from the file provided"""
        control_words = ["fudge", "secret"]
        censor = TextCensor("banned_words.txt")
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
            "There are some words that one must not say such as ***** and ******\n"
        )
        censor = TextCensor("banned_words.txt")

        censor.censor_line_and_print(plain_text)
        self.assertEqual(mock_stdout.getvalue(), censored_text)


if __name__ == "__main__":
    unittest.main()