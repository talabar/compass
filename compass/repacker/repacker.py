import logging
from pathlib import Path
import re
from typing import List

from compass import delimiter as dl
from compass import regex as rx
from compass.datatype import Cipher, TranslateType
from compass.glossary import DEEPL_ERRORS
from compass.repacker.repacker_ltx import LTXRepacker
from compass.repacker.repacker_xml import XMLRepacker
from compass.repacker.repacker_script import ScriptRepacker
from compass.util import get_file_paths

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Repacker:
    def __init__(self, root: Path, mapping: List[str], corpus: List[str], output_root: str):

        self.filenames_xml: List[Path] = get_file_paths(root, ".xml")
        self.filenames_ltx: List[Path] = get_file_paths(root, ".ltx")
        self.filenames_script: List[Path] = get_file_paths(root, ".script")
        self.output_root = output_root

        self.cipher: Cipher = self.create_cipher(mapping, corpus)

    def repack(self):
        xml_repacker = XMLRepacker(self.filenames_xml, self.cipher, self.output_root)
        xml_repacker.repack()

        ltx_repacker = LTXRepacker(self.filenames_ltx, self.cipher, self.output_root)
        ltx_repacker.repack()

        script_repacker = ScriptRepacker(self.filenames_script, self.cipher, self.output_root)
        script_repacker.repack()

    def create_cipher(self, mapping: List[str], corpus: List[str]) -> Cipher:
        self.check_alignment(mapping, corpus)
        self.pre_process(corpus)

        cipher = {}
        num_lines = len(mapping)
        counter = 0

        iter_mapping = iter(mapping)
        iter_corpus = iter(corpus)
        current_file = None

        while counter < num_lines:
            row_mapping = next(iter_mapping)
            row_corpus = next(iter_corpus)

            if re.match(dl.FILE, row_mapping):
                # Create new outer dictionary entry
                current_file = row_mapping.split()[1]
                cipher[current_file] = {}
            elif rx.CIPHER_XML_ARTICLE_NAME.match(row_mapping):
                match = rx.CIPHER_XML_ARTICLE_NAME.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.XML_ARTICLE_NAME
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            elif rx.CIPHER_XML_CATCH_ALL.match(row_mapping):
                match = rx.CIPHER_XML_CATCH_ALL.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.XML_CATCH_ALL
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            elif rx.CIPHER_XML_TEXT_SIMPLE.match(row_mapping):
                match = rx.CIPHER_XML_TEXT_SIMPLE.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.XML_TEXT_SIMPLE
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            elif rx.CIPHER_XML_TEXT_MULTILINE_GENERAL.match(row_mapping):
                match = rx.CIPHER_XML_TEXT_MULTILINE_GENERAL.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.XML_TEXT_MULTILINE_GENERAL
                cipher[current_file][index] = (line_type, row_corpus)
            elif rx.CIPHER_XML_TEXT_MULTILINE_START.match(row_mapping):
                match = rx.CIPHER_XML_TEXT_MULTILINE_START.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.XML_TEXT_MULTILINE_START
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            elif rx.CIPHER_XML_TEXT_MULTILINE_END.match(row_mapping):
                match = rx.CIPHER_XML_TEXT_MULTILINE_END.match(row_mapping)
                index = int(match.groups(1)[0])
                line_type = TranslateType.XML_TEXT_MULTILINE_END
                cipher[current_file][index] = (line_type, row_corpus[:-1])
            elif rx.CIPHER_SCRIPT.match(row_mapping):
                match = rx.CIPHER_SCRIPT.match(row_mapping)
                index_line = int(match.groups()[0])
                index_match = int(match.groups()[1])
                line_type = TranslateType.SCRIPT
                if index_line not in cipher[current_file].keys():
                    cipher[current_file][index_line] = (line_type, {})
                line_mapping = cipher[current_file][index_line][1]
                line_mapping[index_match] = row_corpus[:-1]
            elif rx.CIPHER_LTX_INV_NAME.match(row_mapping):
                match = rx.CIPHER_LTX_INV_NAME.match(row_mapping)
                index = int(match.groups()[0])
                line_type = TranslateType.LTX_INV_NAME
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

    @staticmethod
    def pre_process(corpus: List[str]):
        for idx, text in enumerate(corpus):
            # Hydrate Replacement Vars
            corpus[idx] = corpus[idx].replace(dl.NEWLINE_ESCAPE, "\\\\n")
            corpus[idx] = corpus[idx].replace(dl.NEWLINE, "\\n")
            corpus[idx] = corpus[idx].replace(dl.QUOTATION_ESCAPE, "\\\"")
            corpus[idx] = corpus[idx].replace(dl.QUOTATION, "\"")
            corpus[idx] = corpus[idx].replace(dl.GUILLEMET_LEFT, "«")
            corpus[idx] = corpus[idx].replace(dl.GUILLEMET_RIGHT, "»")
