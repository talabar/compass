import logging
from pathlib import Path
import re
from typing import List

from compass import delimiter as dl
from compass import regex as rx
from compass.datatype import Cipher, TranslateType
from compass.repacker.repacker_ltx import LTXRepacker
from compass.repacker.repacker_xml import XMLRepacker
from compass.util import get_file_paths

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Repacker:
    def __init__(self, root: Path, mapping: List[str], corpus: List[str], output_root: str):

        self.filenames_xml: List[Path] = get_file_paths(root, ".xml")
        self.filenames_ltx: List[Path] = get_file_paths(root, ".ltx")
        self.cipher: Cipher = self.create_cipher(mapping, corpus)
        self.output_root = output_root

    def repack(self):
        xml_repacker = XMLRepacker(self.filenames_xml, self.cipher, self.output_root)
        xml_repacker.repack()

        ltx_repacker = LTXRepacker(self.filenames_ltx, self.cipher, self.output_root)
        ltx_repacker.repack()

    def create_cipher(self, mapping: List[str], corpus: List[str]) -> Cipher:
        self.check_alignment(mapping, corpus)

        cipher = {}
        num_lines = len(mapping)
        counter = 0

        iter_mapping = iter(mapping)
        iter_corpus = iter(corpus)
        current_file = None

        while counter < num_lines:
            row_mapping = next(iter_mapping)
            row_corpus = next(iter_corpus)

            row_corpus = row_corpus.replace(dl.NEWLINE, "\\n")

            if re.match(dl.FILE, row_mapping):
                # Create new outer dictionary entry
                current_file = row_mapping.split()[1]
                cipher[current_file] = {}
            elif rx.CIPHER_SIMPLE.match(row_mapping):
                match = rx.CIPHER_SIMPLE.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.SIMPLE
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            elif rx.CIPHER_MULTILINE_GENERAL.match(row_mapping):
                match = rx.CIPHER_MULTILINE_GENERAL.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.MULTILINE_GENERAL
                cipher[current_file][index] = (line_type, row_corpus)
            elif rx.CIPHER_MULTILINE_START.match(row_mapping):
                match = rx.CIPHER_MULTILINE_START.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.MULTILINE_START
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            elif rx.CIPHER_MULTILINE_END.match(row_mapping):
                match = rx.CIPHER_MULTILINE_END.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.MULTILINE_END
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            else:
                raise Exception(
                    "Cipher Error\nInvalid Mapping\n"
                    f"|{counter}| {row_mapping}"
                )

            counter = counter + 1

        return cipher

    @staticmethod
    def check_alignment(mapping: List[str], corpus: List[str]):
        count_mapping, count_corpus = len(mapping), len(corpus)
        if count_mapping != count_corpus:
            raise Exception(
                "Alignment Error\nLength\n"
                f"Mapping: {count_mapping} <-/-> Corpus: {count_corpus}"
            )
