import argparse
from pathlib import Path

from compass.unpacker.unpacker import UnpackerManager


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
    unpacker = UnpackerManager(args.root, args.outfile)
    unpacker.unpack()


if __name__ == "__main__":
    run()
