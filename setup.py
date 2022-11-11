import setuptools

from better_profanity import __version__

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Text Censor",
    version=__version__,
    author="Aaron Graham",
    author_email="apj_graham@yahoo.co.uk",
    description="Blazingly fast cleaning swear words (and their leetspeak) in strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apj-graham/TextCensor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="==3.*",
    packages=setuptools.find_packages(),
    data_files=[
        ("wordlist", ["better_profanity/profanity_wordlist.txt"]),
    ],
    package_data={"better_profanity": ["profanity_wordlist.txt"]},
    include_package_data=True,
)
