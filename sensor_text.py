import re
import copy


def create_regex_patterns(file):
    patterns_and_replacements = {}

    with open("banned_words.txt") as f:
        for banned_word in f:
            word = banned_word.strip()
            pattern = rf"\b({word})\b"
            stars = "".join(["*" for _ in word])
            patterns_and_replacements[pattern] = stars

    return patterns_and_replacements


def sensor_txt(text, banned_words):
    with open(text) as f:
        for line in f:
            print(line)
            sensored_line = copy.deepcopy(line)
            for pattern, stars in create_regex_patterns(banned_words).items():
                sensored_line = re.sub(pattern, stars, sensored_line, flags=re.IGNORECASE)
            print(sensored_line)





        #with open("prose.txt") as t:
        #    for line in t
        #        line = t.readline()
        #        print(re.sub(pattern, stars, line, flags=re.IGNORECASE))
        #        count += 1




#with open("banned_words.txt") as f:
#    for word in f:
#
#        stars = "".join(["*" for letter in word])
#
#        with open("enwik9") as t:
#            print(type())


if __name__ == "__main__":
    sensor_txt("prose.txt", "banned_words.txt")