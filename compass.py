import argparse
from pathlib import Path

from dotenv import load_dotenv

from src.auditor import XMLAuditor
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
    gpt.add_argument(
        "-raw",
        "--file_raw",
        help="Corpus text file to be translated (line by line)",
        dest="file_raw",
        type=Path,
        required=True,
    )
    gpt.add_argument(
        "-trans",
        "--file_translate",
        help="Output file to store translated text (line by line)",
        type=Path,
        dest="file_translate",
        required=True,
    )
    gpt.add_argument(
        "-ls",
        "--line_start",
        help="Line number with which to start processing (inclusive)",
        dest="start",
        type=int,
        default=0,
        required=False,
    )
    gpt.add_argument(
        "-le",
        "--line_end",
        help="Line number with which to stop processing (exclusive)",
        dest="end",
        type=int,
        required=False,
    )

    # AUDIT
    audit = subparsers.add_parser("audit")
    audit.add_argument(
        "-base",
        "--dir_base",
        dest="dir_base",
        type=Path,
        required=True,
        help="Top directory of base game data",
    )
    audit.add_argument(
        "-trans",
        "--dir_translate",
        dest="dir_translate",
        type=Path,
        required=True,
        help="Top directory of translated game data",
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
        xml_auditor = XMLAuditor(**params)
        xml_auditor.audit()


def start_repack(dir_root: Path, dir_output: Path, file_map: Path, file_translate: Path):
    with open(file_map, "r", encoding="windows-1251") as fp:
        content_map = fp.readlines()
    with open(file_translate, "r", encoding="windows-1251") as fp:
        content_translate = fp.readlines()

    repacker = RepackerManager(dir_root, content_map, content_translate, dir_output)
    repacker.repack()


if __name__ == "__main__":
    load_dotenv()
    run()
