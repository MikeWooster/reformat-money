import argparse
import os

from reformat_money.file_formatter import FileFormatter
from reformat_money.file_searcher import get_files
from reformat_money.settings import EXTENSION


def parse_args_and_reformat():
    args = get_args()
    reformatter(**args)


def get_args() -> dict:  # pragma: no cover
    """Command line argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        type=str,
    )
    args = parser.parse_args()
    return {
        "path": args.path,
    }


def reformatter(path):
    """Recursively get all python files and run reformatting."""

    if os.path.isfile(path) and path.endswith(EXTENSION):
        files = [path]
    elif os.path.isdir(path):
        files = get_files(path)
    else:
        raise RuntimeError(
            f"path provided is not a directory or file, or does not have the correct extension: {path}"
        )
    for file in files:
        formatter = FileFormatter(file)
        formatter.reformat()
