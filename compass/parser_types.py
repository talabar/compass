import argparse
import os


def type_dir(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"|{path}| Not a Valid Directory")


def type_txt(path: str):
    if path.endswith(".txt"):
        return path
    else:
        raise argparse.ArgumentTypeError(f"|{path}| Not a Valid TXT File")
