"""Benchmarks how fast better_profanity censors large bodies of text"""

import os

import pytest
from better_profanity import Profanity


def censor_file(sut):
    text_fp = os.path.join(os.path.dirname(__file__), "../data/bible.txt")
    with open(text_fp) as text_file:
        for line in text_file:
            sut.censor(line)
    
    return True
        
def test_trial(benchmark):
    banned_words_fp = os.path.join(os.path.dirname(__file__), "../data/banned_words.txt")
    sut = Profanity(banned_words_fp)
    
    actual_censored = benchmark(censor_file, sut)

    assert actual_censored != None
    
if __name__ == "__main__":
    pytest.main([__file__])
