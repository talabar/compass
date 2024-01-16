import logging
import re

from src import regex as rx
from src.datatype import TranslateType
from src.repacker.repacker_base import BaseRepacker

LOGGER = logging.getLogger(__name__)


class ScriptRepacker(BaseRepacker):
    def repack(self):
        LOGGER.info("Repacker Script Starting...")

        for filename, translate_instr in self.cipher.items():
            if not filename.endswith(".script"):
                continue

            contents = self.get_base_contents(filename)

            for line_number, (line_type, line_mapping) in translate_instr.items():
                line = contents[line_number - 1]
                if line_type is TranslateType.SCRIPT:
                    for index_match, text in line_mapping.items():
                        line = self._text_replace_nth(rx.SCRIPT_SIMPLE, text, line, index_match)
                else:
                    raise Exception(
                        "Cipher Error\n"
                        "Invalid Translate Type\n"
                        f"|{filename}| [{line_number}] {line_type}"
                    )

                contents[line_number - 1] = line

            LOGGER.info(f"|{filename}| Saving...")
            self.write_contents(filename, contents)

    @staticmethod
    def _text_replace_nth(regex: re.Pattern, text_replace: str, text_old: str, n: int):
        accumulator = -1
        match_iter = regex.finditer(text_old)

        while accumulator < n:
            accumulator = accumulator + 1
            try:
                r = next(match_iter).span(1)
            except StopIteration:
                raise Exception(
                    "Cipher Error\n"
                    "Invalid Mapping For Text Replacement\n"
                    f"New: {text_replace} | Old: {text_old} | Match Index: {n}"
                )
            if accumulator == n:
                return text_old[:r[0]] + text_replace + text_old[r[1]:]

        raise Exception(
            "Cipher Error\n"
            "Invalid Mapping For Text Replacement\n"
            f"New: {text_replace} | Old: {text_old} | Match Index: {n}"
        )
