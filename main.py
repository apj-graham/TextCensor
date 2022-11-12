from better_profanity import Profanity


def main():
    text_censor = Profanity(r"/usr/share/dict/british-english")

    print("Saving regex to file...")
    with open(r"regex.txt", "w") as f:
        f.write(text_censor.censor_regex.pattern)

    with open(r"benchmarking/data/bible.txt") as text:
        while line := text.readline():
            print(text_censor.censor(line), end="")


if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
