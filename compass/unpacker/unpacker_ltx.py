import logging
from pathlib import Path
from typing import List, Match

from compass import regex as rx
from compass.unpacker.unpacker_base import BaseUnpacker
from compass.util import get_file_paths

LOGGER = logging.getLogger(__name__)


class LTXUnpacker(BaseUnpacker):
    def __init__(self, root: Path):
        super().__init__(root)
        self.filenames: List[Path] = get_file_paths(root, ".ltx")

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
