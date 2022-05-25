import logging
from pathlib import Path
from typing import List

from compass import regex as rx
from compass.unpacker.unpacker_base import BaseUnpacker
from compass.util import get_file_paths

LOGGER = logging.getLogger(__name__)


class ScriptUnpacker(BaseUnpacker):
    def __init__(self, root: Path):
        super().__init__(root)
        self.filenames: List[Path] = get_file_paths(root, ".script")

    def unpack_file_contents(self, contents: List[str]):
        for index, line in enumerate(contents, start=1):
            # Ignore Commented Lines
            if rx.SCRIPT_COMMENT.match(line):
                continue
            matches = rx.SCRIPT_SIMPLE.findall(line)

            if matches:
                self.process_match(matches, index)

    def process_match(self, matches: List[str], index_line: int):
        for index_group, match in enumerate(matches):
            if rx.has_cyrillic(match):
                LOGGER.debug(f"|{self.stem}| [{index_line}][{index_group} Match - Script")
                self.line_mapping.append(f"{str(index_line)}_{str(index_group)}\n")
                self.corpus.append(match + "\n")
