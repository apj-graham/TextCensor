from better_profanity import Profanity


def main():
    text_censor = Profanity("../benchmarking/data/banned_words.txt")
    text_censor.construct_censor_regex()
    with open("regex.txt", "w") as f:
        f.write(text_censor.censor_regex.pattern)

    with open("../benchmarking/data/bible.txt") as text:
        while line := text.readline():
            print(text_censor.censor(line), end="")


if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
