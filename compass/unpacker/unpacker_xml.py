import logging
from pathlib import Path
from typing import Iterator, List, Match

from compass import delimiter as dl
from compass import regex as rx
from compass.unpacker.unpacker_base import BaseUnpacker
from compass.util import get_file_paths

LOGGER = logging.getLogger(__name__)


class XMLUnpacker(BaseUnpacker):
    def __init__(self, root: Path):
        super().__init__(root)
        self.filenames: List[Path] = get_file_paths(root, ".xml")

    def unpack_file_contents(self, contents: List[str]):
        line_iter: Iterator[str] = iter(enumerate(contents, start=1))
        for index, line in line_iter:
            match_simple = rx.XML_TEXT_SIMPLE.search(line)
            match_multiline = rx.XML_TEXT_MULTILINE_START.search(line)
            match_pdf_msg = rx.XML_PDF_MSG.search(line)

            if match_simple:
                self.process_simple_match(match_simple, index)
            elif match_multiline:
                self.process_multiline_match(match_multiline, index, line_iter)
            elif match_pdf_msg:
                self.process_pdf_msg(match_pdf_msg, index)

        # self.post_process()

    def process_simple_match(self, match: Match, index: int):
        text = match.groups()[0]

        if rx.has_cyrillic(text):
            LOGGER.debug(f"|{self.stem}| [{index}] Match - Simple")
            self.line_mapping.append(str(index) + "\n")
            self.corpus.append(text + "\n")

    def process_pdf_msg(self, match: Match, index: int):
        text = match.groups()[0]

        if rx.has_cyrillic(text):
            LOGGER.debug(f"|{self.stem}| [{index}] Match - PDF MSG")
            self.line_mapping.append(str(index) + dl.PDF_MSG + "\n")
            self.corpus.append(text + "\n")

    def process_multiline_match(self, match: Match, index: int, line_iter: Iterator[str]):
        # Handle Starting Line
        text_start = match.groups()[0]
        if text_start and rx.has_cyrillic(text_start):
            LOGGER.debug(f"|{self.stem}| [{index}] Match - Multiline: Start")
            self.line_mapping.append(str(index) + dl.MULTILINE_START + "\n")
            self.corpus.append(text_start + "\n")

        # Handle Middle Line(s)
        index, line = next(line_iter)
        while not rx.XML_TEXT_MULTILINE_END.search(line):
            if rx.has_cyrillic(line):
                LOGGER.debug(f"|{self.stem}| [{index}] Match - Multiline: General")
                text = line[:-1] if line.endswith("\n") else line
                self.line_mapping.append(str(index) + dl.MULTILINE_GENERAL + "\n")
                self.corpus.append(text + "\n")
            try:
                index, line = next(line_iter)
            except StopIteration:
                return

        # Handle End Line
        match_end = rx.XML_TEXT_MULTILINE_END.search(line)
        text_end = match_end.groups()[0]
        if text_end and rx.has_cyrillic(text_end):
            LOGGER.debug(f"|{self.stem}| [{index}] Match - Multiline: End")
            self.line_mapping.append(str(index) + dl.MULTILINE_END + "\n")
            self.corpus.append(text_end + "\n")

