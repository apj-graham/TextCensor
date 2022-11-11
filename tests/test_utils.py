import unittest

from better_profanity import utils


class TestUtils(unittest.TestCase):
    """Test for the Utility functions"""

    def test_read_word_list(self):
        """Words are read from a file and the white space is stripped"""
        filepath = r"data\small_word_list.txt"

        expected_words = ["these", "are", "some", "words"]
        words = [word for word in utils.read_wordlist(filepath)]

        self.assertEqual(expected_words, words)

    def test_get_complete_path_of_file(self):
        """Filepath is extended to include the full path"""
        filepath = r"data\small_word_list.txt"

        extended_file_path = utils.get_complete_path_of_file(filepath)
        elements = extended_file_path.split("\\")
        
        # Check that top level project directory is included
        self.assertTrue("better_profanity" in elements)
        self.assertGreater(len(elements), 3)