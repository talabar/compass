import argparse
from pathlib import Path

from compass.repacker.repacker import Repacker


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-root",
        help="Parent directory containing base XML files",
        dest="root",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-out",
        help="Output Directory",
        dest="outdir",
        required=True,
    )
    parser.add_argument(
        "-map",
        help="Mapping File",
        dest="mapping",
        required=True,
    )
    parser.add_argument(
        "-text",
        help="Translated Text Corpus",
        dest="text",
        required=True,
    )
    args = parser.parse_args()

    with open(args.mapping, "r", encoding="windows-1251") as fp:
        mapping = fp.readlines()
    with open(args.text, "r", encoding="windows-1251") as fp:
        text = fp.readlines()

    repacker = Repacker(args.root, mapping, text, args.outdir)
    repacker.repack()


if __name__ == "__main__":
    run()
