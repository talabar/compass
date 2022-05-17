import logging
from pathlib import Path
from typing import List, Match, Tuple

from compass import delimiter as dl
from compass import regex as rx
from compass.util import get_file_title

LOGGER = logging.getLogger(__name__)


class LTXUnpacker:
    def __init__(self, filenames: List[Path]):
        self.filenames = filenames
        self.stem = None
        self.line_mapping = []
        self.corpus = []

    def unpack(self) -> Tuple[List[str], List[str]]:
        LOGGER.info(f"LTX Unpacker Starting...")

        for filename in self.filenames:

            self.stem = filename.stem

            LOGGER.info(f"|{self.stem}| Loading...")
            with open(filename, "r", encoding="windows-1251", errors="ignore") as input_fp:
                file_contents = input_fp.readlines()

            file_title = dl.FILE + " " + get_file_title(filename) + "\n"
            self.line_mapping.append(file_title)
            self.corpus.append(file_title)

            self.unpack_file_contents(file_contents)

            if self.line_mapping[-1] == file_title:
                self.line_mapping.pop()
                self.corpus.pop()
            else:
                LOGGER.info(f"|{self.stem}| Unpacked Successfully")

        return self.line_mapping, self.corpus

    def unpack_file_contents(self, contents: List[str]):
        for index, line in enumerate(contents, start=1):
            match_inv_name = rx.LTX_INV_NAME.match(line)

            if match_inv_name:
                self.process_match_inv_name(match_inv_name, index)

    def process_match_inv_name(self, match: Match, index: int):
        text = match.groups()[0]

        if rx.has_cyrillic(text):
            LOGGER.debug(f"|{self.stem}| [{index}] Match - Inv Name")
            self.line_mapping.append(str(index) + "\n")
            self.corpus.append(text + "\n")
