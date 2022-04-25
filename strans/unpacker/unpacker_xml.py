import logging
from pathlib import Path
from typing import Iterator, List, Match, Tuple

from strans import delimiter as dl
from strans import rx
from strans.util import get_file_title

LOGGER = logging.getLogger(__name__)


class XMLUnpacker:
    def __init__(self, filenames: List[Path]):
        self.filenames = filenames
        self.stem = None
        self.line_mapping = []
        self.corpus = []

    def unpack(self) -> Tuple[List[str], List[str]]:
        LOGGER.info(f"Starting...")

        for filename in self.filenames:

            self.stem = filename.stem

            LOGGER.info(f"|{self.stem}| Loading...")

            with open(filename, "r", encoding="windows-1251", errors="ignore") as input_fp:
                file_contents = input_fp.readlines()

            file_title = dl.FILE_LEFT + " " + get_file_title(filename) + "\n"
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
        line_iter: Iterator[str] = iter(enumerate(contents, start=1))
        for index, line in line_iter:
            match_simple = rx.XML_SIMPLE.search(line)
            match_multiline = rx.XML_MULTILINE_START.search(line)

            if match_simple:
                self.process_simple_match(match_simple, index)
            elif match_multiline:
                self.process_multiline_match(match_multiline, index, line_iter)
            else:
                continue

        self.post_process()

    def process_simple_match(self, match: Match, index: int):
        text = match.groups()[0]

        if rx.has_cyrillic(text):
            LOGGER.debug(f"|{self.stem}| [{index}] Match - Simple")
            self.line_mapping.append(str(index) + "\n")
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
        while not rx.XML_MULTILINE_END.search(line):
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
        match_end = rx.XML_MULTILINE_END.search(line)
        text_end = match_end.groups()[0]
        if text_end and rx.has_cyrillic(text_end):
            LOGGER.debug(f"|{self.stem}| [{index}] Match - Multiline: End")
            self.line_mapping.append(str(index) + dl.MULTILINE_END + "\n")
            self.corpus.append(text_end + "\n")

    def post_process(self):
        for idx, text in enumerate(self.corpus):
            self.corpus[idx] = text.replace("\\n", dl.NEWLINE)
