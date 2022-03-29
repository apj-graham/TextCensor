"""Unit tests for the imput validation"""

import os
import unittest
from unittest.mock import call, patch

from src.input_validation import validate_arguments, validate_filepath


class TestInputValidation(unittest.TestCase):
    """Unit tests for the imput validation"""

    def test_valid_text_file(self):
        """The file path to and existing text file does not raise an error"""
        validate_filepath(os.path.abspath("test/test_resources/sample_text.txt"))

    def test_non_existant_file(self):
        """A filepath that does not exist raises an IOError"""
        with self.assertRaises(IOError):
            validate_filepath(
                os.path.abspath("test/test_resources/non_existent_text.txt")
            )

    def test_non_text_file(self):
        """A file that is not a text file raises an IOError"""
        with self.assertRaises(IOError):
            validate_filepath(os.path.abspath("test/test_resources/non_test_file.png"))

    @patch("src.input_validation.validate_filepath")
    def test_validate_arguments_function_calls(self, validate_filepath):
        """Validate arguments calls validate_file_path for each filepath passed
        to it"""
        test_args = [
            os.path.abspath("test/test_resources/sample_text.txt"),
            os.path.abspath("test/test_resources/banned_words.txt"),
        ]
        expected_calls = [call(test_args)]
        validate_arguments(test_args)
        validate_filepath.assert_has_calls(expected_calls)
