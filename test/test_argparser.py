"""Unit tests for the arg parser"""

import sys
import unittest
from argparse import Namespace
from unittest.mock import patch

from src.arg_parser import parse_arguments


class TestArgParser(unittest.TestCase):
    """Unit Tests for the arg parser"""

    @patch.object(sys, "argv", ["prog", "test_string1", "test_string2"])
    def test_arg_parser(self):
        """Parser returns two strings when given two strings"""
        expected_result = {
            "banned_words_file": "test_string1",
            "document": "test_string2",
        }
        args = parse_arguments()
        self.assertIsInstance(args, Namespace)

        self.assertTrue(hasattr(args, "banned_words_file"))
        self.assertIsInstance(args.banned_words_file, str)

        self.assertTrue(hasattr(args, "document"))
        self.assertIsInstance(args.document, str)

        self.assertDictEqual(expected_result, vars(args))
