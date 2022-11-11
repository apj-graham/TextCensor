# -*- coding: utf-8 -*-

import os.path
from itertools import product

from .constants import CHAR_MAP


def get_complete_path_of_file(filename):
    """Join the path of the current directory with the input filename."""
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, filename)


def read_wordlist(filename: str):
    """Return words from a wordlist file."""
    with open(filename, encoding="utf-8") as wordlist_file:
        for row in wordlist_file:
            row = row.strip()
            if row != "":
                yield row


def get_leet_combinations(word):
    """Get all combinations of leet character substitutions for a word

    https://stackoverflow.com/q/44181772"""
    combos = [(char,) if char not in CHAR_MAP else CHAR_MAP[char] for char in word]
    return ("".join(o) for o in product(*combos))
