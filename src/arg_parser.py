import argparse


def parse_arguments():
    """Process command line arguments using Python standard argument parser

    Returns:
        Parsed args: list
            List of argumments entered in the command line
    """
    parser = argparse.ArgumentParser(description="Text Sensorer")
    parser.add_argument(
        "banned_words_file",
        type=str,
        help="Text file with a lost of banned words, one per line",
    )
    parser.add_argument("document", type=str, help="Text file with text to sensor")
    return parser.parse_args()
