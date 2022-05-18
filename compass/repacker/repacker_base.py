from abc import ABC, abstractmethod
import logging
import os
from pathlib import Path
import re
from typing import List

from compass.datatype import Cipher

LOGGER = logging.getLogger(__name__)


class BaseRepacker(ABC):
    def __init__(self, filenames: List[Path], cipher: Cipher, output_root: str):
        self.filenames_base = filenames
        self.cipher = cipher
        self.output_root = output_root

    @abstractmethod
    def repack(self):
        pass

    def write_contents(self, filename: str, contents: List[str]):
        # Prepend Output Root to Filename
        write_path = Path(self.output_root + os.path.sep + filename)

        # Generate all subdirectories from output root
        write_path.parents[0].mkdir(parents=True, exist_ok=True)

        with open(write_path, "w+", encoding="windows-1251") as fp:
            fp.writelines(contents)

    def get_base_contents(self, filename: str):
        filename_base = None
        for filename_candidate in self.filenames_base:
            if str(filename_candidate.resolve()).endswith(filename):
                filename_base = filename_candidate
                break

        if not filename_base:
            raise Exception(f"File Not Found: {filename}")

        with open(filename_base, "r", encoding="windows-1251") as fp:
            contents_base = fp.readlines()

        return contents_base

    @staticmethod
    def _text_replace(regex: re.Pattern, text_replace: str, text_old: str):
        r = regex.search(text_old).span(1)
        text_new = text_old[:r[0]] + text_replace + text_old[r[1]:]
        return text_new
