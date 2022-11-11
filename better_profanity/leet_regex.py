import re
from itertools import product

from .constants import CHAR_MAP


def get_leet_combinations(word):
    """Get all combinations of leet character substitutions for a word
    
    https://stackoverflow.com/q/44181772"""
    combos = [(char,) if char not in CHAR_MAP else CHAR_MAP[char] for char in word]
    return (''.join(o) for o in product(*combos))

class LeetTrie():
    """Regex::Trie in Python. Creates a Trie out of a list of words. The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union.
    
    https://stackoverflow.com/a/42789508"""

    def __init__(self):
        self.data = {}

    def add(self, word):
        ref = self.data
        for leet in get_leet_combinations(word):
            for char in leet:
                ref[char] = char in ref and ref[char] or {}
                ref = ref[char]
            ref[''] = 1
    
    def add_words(self, word_list):
        for word in word_list:
            self.add(word)

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self.quote(char) + recurse)
                except:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append('[' + ''.join(cc) + ']')

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())

if __name__ == "__main__":
    trie = LeetTrie()
    trie.add("pie")
    print(trie.pattern())
