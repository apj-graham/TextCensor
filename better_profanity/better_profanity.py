# -*- coding: utf-8 -*-

import os
import re
from collections.abc import Iterable

from .leet_regex import LeetTrie
from .utils import get_complete_path_of_file, read_wordlist, get_leet_combinations


class Profanity:

    def __init__(self, words=None):
        """
        Args:
            words (Iterable/str): Collection of words or file path for a list of
                words to censor. `None` to use the default word list.

        Raises:
            TypeError: If `words` is not a valid type.
            FileNotFoundError: If `words` is a `str` and is not a valid file path.
        """
        if (
            words is not None
            and not isinstance(words, str)
            and not isinstance(words, Iterable)
        ):
            raise TypeError("words must be of type str, list, or None")
        self.CENSOR_WORDSET = []
        self._default_wordlist_filename = get_complete_path_of_file(
            "profanity_wordlist.txt"
        )
        self.load_censor_words(words)

        self.censor_regex = self.construct_censor_regex()

    def load_censor_words(self, source=None):
        if isinstance(source, str):
            if not os.path.isfile(source):
                raise FileNotFoundError("Path provided is not a file")
            else:
                words = read_wordlist(source)
                self._populate_words_to_wordset(words)
        elif isinstance(source, Iterable):
            self._populate_words_to_wordset(source)
        else:
            words = read_wordlist(self._default_wordlist_filename)
            self._populate_words_to_wordset(words)

    def _populate_words_to_wordset(self, words):
        censor_words = [word.lower() for word in set(words)]
        all_censor_words = []
        for word in censor_words:
            for leet_word in get_leet_combinations(word):
                all_censor_words.append(leet_word)

        all_censor_words.sort()
        # The default wordlist takes ~5MB+ of memory
        self.CENSOR_WORDSET = all_censor_words

    def construct_censor_regex(self):
        """Create compiled regex to match banned words"""
        trie = LeetTrie()
        trie.add_words(self.CENSOR_WORDSET)
        return re.compile(r"\b" + trie.pattern() + r"\b", re.IGNORECASE)

    def censor(self, text, censor_char="*"):
        """Replace the swear words in the text with `censor_char`."""

        if not isinstance(text, str):
            text = str(text)
        if not isinstance(censor_char, str):
            censor_char = str(censor_char)

        if not self.CENSOR_WORDSET:
            self.load_censor_words()

        return self._hide_swear_words(text, censor_char, self.censor_regex)

    def _hide_swear_words(self, text, censor_char, censor_pattern):
        """Replace the swear words with censor characters."""
        repl_func = lambda line: censor_char * len(line.group())
        words = [censor_pattern.sub(repl_func, word) for word in text.split(" ")]
        return " ".join(words)

    def contains_profanity(self, text):
        """Return True if  the input text has any swear words."""
        return text != self.censor(text)
