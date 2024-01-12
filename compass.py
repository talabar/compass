import argparse
from pathlib import Path

from src.gpt import GPTTranslator
from src.unpacker.unpacker_manager import UnpackerManager
from src.repacker.repacker_manager import RepackerManager


def run():
    args = get_args()
    dispatch(args)


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    # UNPACK
    unpack = subparsers.add_parser("unpack")
    unpack.add_argument(
        "-root",
        dest="dir_root",
        type=Path,
        required=True,
        help="Parent directory containing desired translation files",
    )
    unpack.add_argument(
        "-out",
        dest="prefix_output",
        required=True,
        help="Prefix for output corpus file & map file",
    )

    # REPACK
    repack = subparsers.add_parser("repack")
    repack.add_argument(
        "-root",
        dest="dir_root",
        type=Path,
        required=True,
        help="Path of parent directory containing untranslated gamedata files",
    )
    repack.add_argument(
        "-out",
        dest="dir_output",
        required=True,
        help="Path of to-be-translated gamedata files",
    )
    repack.add_argument(
        "-map",
        dest="file_map",
        required=True,
        help="Path of mapping file (created by unpack step)",
    )
    repack.add_argument(
        "-trans",
        dest="file_translate",
        required=True,
        help="Path of translated file",
    )

    # GPT
    gpt = subparsers.add_parser("gpt")
    parser.add_argument(
        "-raw",
        "--rawfile",
        help="Corpus text file to be translated (line by line)",
        dest="rawfile",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-out",
        "--outfile",
        help="Output file to store translated text (line by line)",
        type=Path,
        dest="outfile",
        required=True,
    )
    parser.add_argument(
        "-ls",
        "--linestart",
        help="Line number with which to start processing (inclusive)",
        dest="start",
        type=int,
        default=0,
        required=False,
    )
    parser.add_argument(
        "-le",
        "--lineend",
        help="Line number with which to stop processing (exclusive)",
        dest="end",
        type=int,
        required=False,
    )

    return vars(parser.parse_args())


def dispatch(params: dict):
    action = params.pop("action")
    if action == "unpack":
        unpacker = UnpackerManager(**params)
        unpacker.unpack()
    if action == "repack":
        start_repack(**params)
    if action == "gpt":
        gpt = GPTTranslator(**params)
        gpt.translate()
    if action == "audit":
        pass


def start_repack(dir_root: Path, dir_output: Path, file_map: Path, file_translate: Path):
    with open(file_map, "r", encoding="windows-1251") as fp:
        content_map = fp.readlines()
    with open(file_translate, "r", encoding="windows-1251") as fp:
        content_translate = fp.readlines()

    repacker = RepackerManager(dir_root, content_map, content_translate, dir_output)
    repacker.repack()


if __name__ == "__main__":
    run()
