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
        "-map-xml",
        help="Mapping File for XML Content",
        dest="mapping_xml",
        required=True,
    )
    parser.add_argument(
        "-text-xml",
        help="Translated Text Corpus",
        dest="text_xml",
        required=True,
    )
    args = parser.parse_args()

    with open(args.mapping_xml, "r", encoding="windows-1251") as fp:
        mapping_xml = fp.readlines()
    with open(args.text_xml, "r", encoding="windows-1251", errors="ignore") as fp:
        text_xml = fp.readlines()

    repacker = Repacker(args.root, mapping_xml, text_xml, args.outdir)
    repacker.repack()


if __name__ == "__main__":
    run()
