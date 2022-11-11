
import unittest

from better_profanity import Profanity


class TestProfanity(unittest.TestCase):
    """Test for the "Profanity" class and it's methods"""

    def test_init_with_defaults(self):
        """Class initialised with default values does not raise errors"""
        try:
            Profanity()
        except Exception as e:
            self.fail(f"__init__() raised {e} unexpectedly")

    def test_init_with_iterable(self):
        """Class initialised with iterable does not raise errors"""
        custom_bad_words = ["happy", "jolly", "merry"]
        try:
            Profanity(custom_bad_words)
        except Exception as e:
            self.fail(f"__init__() raised {e} unexpectedly")
    
    def test_init_with_file_path(self):
        """Class initialised with iterable does not raise errors"""
        file_path = "data/small_word_list.txt"
        try:
            Profanity(file_path)
        except Exception as e:
            self.fail(f"__init__() raised {e} unexpectedly")

    def test_init_with_bad_type(self):
        """Class initialised with invalid valued raises a TypeError"""
        with self.assertRaises(TypeError):
            Profanity(False)

    def test_load_censor_words_file(self):
        """List of words to be censored is populated with those from the provided iterable"""
        file_path = "data/small_word_list.txt"
        sut = Profanity(file_path)

        expected_banned_words = ["are", "some", "these", "words"]
        self.assertEqual(expected_banned_words, sut.CENSOR_WORDSET)
    
    def test_load_censor_words_invalid_file(self):
        """List of words to be censored is populated with those from the provided iterable"""
        file_path = "not_a_file.txt"
        with self.assertRaises(FileNotFoundError):
            sut = Profanity(file_path)

    def test_load_censor_words_iterable(self):
        """List of words to be censored is populated with those from the provided iterable"""
        custom_bad_words = ["happy", "jolly", "merry"]
        sut = Profanity(custom_bad_words)

        self.assertEqual(custom_bad_words, sut.CENSOR_WORDSET)
    
    def test_load_censor_words_duplicates(self):
        """List of words to be censored is populated with those from the provided iterable"""
        custom_bad_words = ["happy", "jolly", "merry", "jolly"]
        sut = Profanity(custom_bad_words)

        expected_banned_words = ["happy", "jolly", "merry"]
        self.assertEqual(expected_banned_words, sut.CENSOR_WORDSET)

    def test_load_censor_words_new_words_overwrite(self):
        """Loading new words overwrites existing word list"""
        sut = Profanity(["bar", "foo"])
        self.assertEqual(sut.CENSOR_WORDSET, ["bar", "foo"])

        sut.load_censor_words(["other", "words"])
        self.assertEqual(sut.CENSOR_WORDSET, ["other", "words"])

    def test_construct_censor_regex(self):
        """For the given words, the regex pattern is comprised of those words(including variations)"""
        sut = Profanity(["a", "b"])
        expected_regex_pattern = r"\b(?:a(?:@(?:\*4?)?)?|b)\b"

        self.assertEqual(expected_regex_pattern, sut.censor_regex.pattern)
    
    def test_hide_swear_words(self):
        """Banned words are replaced with an equal number of a given character"""
        sut = Profanity(["a", "test"])
        text = "This is a test"
        
        expected_censored_text = "This is * ****"
        censored_text = sut._hide_swear_words(text, "*", sut.censor_regex)

        self.assertEqual(expected_censored_text, censored_text)
    
    def test_contains_profanity(self):
        """Returns True is banned words are present, else False"""
        sut = Profanity(["a", "test"])
        profane_text = "This is a test"
        non_profane_text = "This is some text"
        
        self.assertTrue(sut.contains_profanity(profane_text))
        self.assertFalse(sut.contains_profanity(non_profane_text))

    def test_censor_simple_case(self):
        """Banned words are redacted in given text"""
        sut = Profanity(["a", "test"])
        text = "This is a test"
        
        expected_text = "This is * ****"
        censored_text = sut.censor(text)
        
        self.assertEqual(expected_text, censored_text)
    
    def test_censor_leet_speak(self):
        """Banned words with alternative letters are redacted in given text"""
        sut = Profanity(["a", "test"])
        text = "This is @ test"
        
        expected_text = "This is * ****"
        censored_text = sut.censor(text)

        self.assertEqual(expected_text, censored_text)

    def test_censor_paragraph(self):
        """Censored text retains new lines"""
        sut = Profanity()
        innocent_text = """If you tickle us do we not laugh?
                        If you poison us do we not die?
                        And if you wrong us shall we not revenge?"""
        censored_text = sut.censor(innocent_text)
        self.assertEqual(innocent_text, censored_text)

    def test_censor_empty_string(self):
        """Empty string remains unchanged"""
        sut = Profanity()
        censored_text = sut.censor("")
        self.assertEqual(censored_text, "")

    def test_censor_clean_text(self):
        """Clean text remains unchanged"""
        sut = Profanity()
        clean_text = "Hi there"
        self.assertEqual(sut.censor(clean_text), clean_text)

    def test_censorship_without_spaces(self):
        """Banned words substrings are redacted"""
        sut = Profanity(["foo"])
        bad_text = "abcfoodef"
        censored_text = "abcfoodef"
        self.assertEqual(sut.censor(bad_text), censored_text)
    
    def test_censor_unicode_cyrillic(self):
        """Cyrillic characters are redacted"""
        sut = Profanity(["хайль"])
        bad_text = "соседский мальчик сказал хайль и я опешил."
        censored_text = "соседский мальчик сказал ***** и я опешил."
        self.assertEqual(sut.censor(bad_text), censored_text)

    def test_censor_unicode_vietnamese(self):
        """Latin based Vietnamese characters are redacted"""
        sut = Profanity(["câu", "bậy"])
        bad_text = "Đây là 1 câu nói bậy."
        censored_text = "Đây là 1 *** nói ***."
        self.assertEqual(sut.censor(bad_text), censored_text)

if __name__ == "__main__":
    unittest.main()
