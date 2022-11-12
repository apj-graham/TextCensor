import unittest

from better_profanity import constants, utils


class TestUtils(unittest.TestCase):
    """Test for the Utility functions"""

    def test_read_word_list(self):
        """Words are read from a file and the white space is stripped"""
        filepath = utils.get_complete_path_of_file(r"../tests/data/small_word_list.txt")

        expected_words = ["word"]
        words = [word for word in utils.read_wordlist(filepath)]

        self.assertEqual(expected_words, words)

    def test_get_complete_path_of_file(self):
        """Filepath is extended to include the full path"""
        filepath = r"./data/small_word_list.txt"

        extended_file_path = utils.get_complete_path_of_file(filepath)
        elements = extended_file_path.split("/")

        # Check that top level project directory is included
        self.assertTrue("better_profanity" in elements)
        self.assertGreater(len(elements), 3)

    def test_get_leet_combinations(self):
        """All combinations of leet character substitutions are returned"""
        for letter, alts in constants.CHAR_MAP.items():
            self.assertCountEqual(alts, list(utils.get_leet_combinations(letter)))

    def test_get_leet_combinations_word(self):
        """All combinations of leet character substitutions for a word are returned"""
        self.maxDiff = None
        words = list(utils.get_leet_combinations("Aioli"))
        expected_words = [
            "Aioli",
            "Aiol*",
            "Aioll",
            "Aiol1",
            "Aio1i",
            "Aio1*",
            "Aio1l",
            "Aio11",
            "Ai*li",
            "Ai*l*",
            "Ai*ll",
            "Ai*l1",
            "Ai*1i",
            "Ai*1*",
            "Ai*1l",
            "Ai*11",
            "Ai0li",
            "Ai0l*",
            "Ai0ll",
            "Ai0l1",
            "Ai01i",
            "Ai01*",
            "Ai01l",
            "Ai011",
            "Ai@li",
            "Ai@l*",
            "Ai@ll",
            "Ai@l1",
            "Ai@1i",
            "Ai@1*",
            "Ai@1l",
            "Ai@11",
            "A*oli",
            "A*ol*",
            "A*oll",
            "A*ol1",
            "A*o1i",
            "A*o1*",
            "A*o1l",
            "A*o11",
            "A**li",
            "A**l*",
            "A**ll",
            "A**l1",
            "A**1i",
            "A**1*",
            "A**1l",
            "A**11",
            "A*0li",
            "A*0l*",
            "A*0ll",
            "A*0l1",
            "A*01i",
            "A*01*",
            "A*01l",
            "A*011",
            "A*@li",
            "A*@l*",
            "A*@ll",
            "A*@l1",
            "A*@1i",
            "A*@1*",
            "A*@1l",
            "A*@11",
            "Aloli",
            "Alol*",
            "Aloll",
            "Alol1",
            "Alo1i",
            "Alo1*",
            "Alo1l",
            "Alo11",
            "Al*li",
            "Al*l*",
            "Al*ll",
            "Al*l1",
            "Al*1i",
            "Al*1*",
            "Al*1l",
            "Al*11",
            "Al0li",
            "Al0l*",
            "Al0ll",
            "Al0l1",
            "Al01i",
            "Al01*",
            "Al01l",
            "Al011",
            "Al@li",
            "Al@l*",
            "Al@ll",
            "Al@l1",
            "Al@1i",
            "Al@1*",
            "Al@1l",
            "Al@11",
            "A1oli",
            "A1ol*",
            "A1oll",
            "A1ol1",
            "A1o1i",
            "A1o1*",
            "A1o1l",
            "A1o11",
            "A1*li",
            "A1*l*",
            "A1*ll",
            "A1*l1",
            "A1*1i",
            "A1*1*",
            "A1*1l",
            "A1*11",
            "A10li",
            "A10l*",
            "A10ll",
            "A10l1",
            "A101i",
            "A101*",
            "A101l",
            "A1011",
            "A1@li",
            "A1@l*",
            "A1@ll",
            "A1@l1",
            "A1@1i",
            "A1@1*",
            "A1@1l",
            "A1@11",
        ]

        self.assertEqual(expected_words, words)
