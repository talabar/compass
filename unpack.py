import argparse
from pathlib import Path

from strans.parser_types import type_txt
from strans.unpacker.unpacker import Unpacker


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-root",
        help="Parent directory containing desired translation files",
        dest="root",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-out",
        help="Output file path stem",
        dest="outfile",
        required=True,
    )
    args = parser.parse_args()
    unpacker = Unpacker(args.root, args.outfile)
    unpacker.unpack()


if __name__ == "__main__":
    run()
