import unittest

from better_profanity.trie import Trie


class TestTrie(unittest.TestCase):
    """Test for the Trie class"""

    def test_add_single_word(self):
        """Single word added in the form of a nested dict"""
        sut = Trie()

        sut.add("happy")
        expected_dict = {"h": {"a": {"p": {"p": {"y": {"": 1}}}}}}

        self.assertEqual(expected_dict, sut.data)

    def test_add_multiple_words(self):
        """Two words added in the form of a nested dict"""
        sut = Trie()

        sut.add("happy")
        sut.add("halted")
        expected_dict = {
            "h": {"a": {"l": {"t": {"e": {"d": {"": 1}}}}, "p": {"p": {"y": {"": 1}}}}}
        }

        self.assertEqual(expected_dict, sut.data)

    def test_add_words_from_iterable(self):
        """Two words added in the form of a nested dict"""
        sut = Trie()

        sut.add_words(["happy", "halted"])
        expected_dict = {
            "h": {"a": {"l": {"t": {"e": {"d": {"": 1}}}}, "p": {"p": {"y": {"": 1}}}}}
        }

        self.assertEqual(expected_dict, sut.data)

    def test_dump(self):
        """dump method returns trie dict stored in Trie class"""
        sut = Trie()

        sut.add("happy")
        expected_dict = {"h": {"a": {"p": {"p": {"y": {"": 1}}}}}}

        self.assertEqual(expected_dict, sut.dump())
        self.assertEqual(sut.data, sut.dump())

    def test_quote_non_control_char(self):
        """Non regex control characters are unchanged"""
        sut = Trie()

        expected_result = r"A"
        self.assertEqual(expected_result, sut.quote("A"))

    def test_quote_control_char(self):
        """Regex control characters have \ appended to them"""
        sut = Trie()

        expected_result = r"\*"
        self.assertEqual(expected_result, sut.quote("*"))

    def test_pattern(self):
        sut = Trie()
        sut.add_words(["happy", "halted"])

        pattern = sut.pattern()
        expected_pattern = r"ha(?:lted|ppy)"

        self.assertEqual(expected_pattern, pattern)

    def test_words(self):
        """Words added to Trie are returned in a list"""
        words = ["happy", "halted"]
        sut = Trie()
        sut.add_words(words)

        self.assertCountEqual(words, sut.words())
