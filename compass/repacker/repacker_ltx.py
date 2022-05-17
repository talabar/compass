import logging
import os
from pathlib import Path
import re
from typing import List

from compass import regex as rx
from compass.datatype import Cipher, TranslateType

LOGGER = logging.getLogger(__name__)


class LTXRepacker:
    def __init__(self, filenames: List[Path], cipher: Cipher, output_root: str):
        self.filenames_base = filenames
        self.cipher = cipher
        self.output_root = output_root

    def repack(self):
        LOGGER.info("Repacker LTX Starting...")

        for filename, translate_instr in self.cipher.items():
            if not filename.endswith(".ltx"):
                continue

            contents = self.get_base_contents(filename)

            for line_number, (line_type, text) in translate_instr.items():
                line = contents[line_number - 1]
                if line_type is TranslateType.SIMPLE:
                    line_translate = self._text_replace(rx.LTX_INV_NAME, text, line)
                else:
                    raise Exception(
                        "Cipher Error\n"
                        "Invalid Translate Type\n"
                        f"|{filename}| [{line_number}] {line_type}"
                    )

                contents[line_number - 1] = line_translate

            LOGGER.info(f"|{filename}| Saving...")
            self.write_contents(filename, contents)

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
