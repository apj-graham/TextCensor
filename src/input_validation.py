"""Utility functions to validate input parameters"""

import os

import magic


def validate_arguments(*files):
    """Check files entered in command line exist and are the correct type

    Arguments:
        files: list
            List of files to to be used
    """
    for file in files:
        validate_filepath(file)


def validate_filepath(filepath):
    """
    Checks the given filepath exists and that the file at that path is a text file

    Parameters
    ----------
    filepath : str
        The file path to be validated

    Returns
    -------
    None

    Raises
    ------
    IOError
    """
    # Check filepath exists
    if not os.path.exists(filepath):
        raise IOError(f"{filepath} does not exist.")

    # Check file given is a text file. Note, text files may not have the .txt
    # file extension so we have to check the file type
    file_type = magic.from_file(filepath, mime=True)
    if "text" not in file_type:
        raise IOError(
            f"File provided is not a text file. File given was a {file_type} file"
        )
