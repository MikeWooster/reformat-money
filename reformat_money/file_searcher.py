import os

from reformat_money.settings import EXTENSION


def get_files(dirname):
    files = []
    for basename in os.listdir(dirname):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename) and filename.endswith(EXTENSION):
            files.append(filename)
        elif os.path.isdir(filename):
            files.extend(get_files(filename))
    return files
