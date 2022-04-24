import logging
from pathlib import Path
from typing import Iterator, List, Match

from strans import delimiter as dl
from strans import rx
from strans.util import get_file_title

LOGGER = logging.getLogger(__name__)


class XMLUnpacker:
    def __init__(self, filenames: List[Path]):
        self.filenames = filenames
        self.stem = None

    def unpack(self) -> List[str]:
        unpack_xml = []

        for filename in self.filenames:

            self.stem = filename.stem

            LOGGER.info(f"|{self.stem}| Loading...")

            with open(filename, "r", encoding="windows-1251", errors="ignore") as input_fp:
                file_contents = input_fp.readlines()
            file_title = get_file_title(filename)

            file_contents_unpack = self.unpack_file_contents(file_contents)

            if file_contents_unpack:
                LOGGER.info(f"|{self.stem}| Unpacked Successfully")
                unpack_xml.append(file_title + "\n")
                unpack_xml += file_contents_unpack

        return unpack_xml

    def unpack_file_contents(self, contents: List[str]) -> List[str]:
        contents_unpack = []

        line_iter: Iterator[str] = iter(enumerate(contents, start=1))
        for idx, line in line_iter:
            match_simple = rx.XML_SIMPLE.search(line)
            match_multiline = rx.XML_MULTILINE_START.search(line)

            if match_simple:
                text = self.process_simple_match(match_simple, idx)
                if not rx.has_cyrillic(text):
                    continue
                LOGGER.debug(f"|{self.stem}| [{idx}] Match - Simple")
            elif match_multiline:
                list_multiline = self.process_multiline_match(match_multiline, idx, line_iter)
                text = "\n".join(list_multiline)
                if not rx.has_cyrillic(text):
                    continue
                LOGGER.debug(f"|{self.stem}| [{idx}] Match - Multiline")
            else:
                continue

            contents_unpack.append(text)

        return contents_unpack

    @staticmethod
    def process_simple_match(match: Match, idx: int) -> str:
        prefix = f"[{idx}]"
        text = match.groups()[0]
        text_format = prefix + " " + text + "\n"
        return text_format

    @staticmethod
    def process_multiline_match(match: Match, idx: int, line_iter: Iterator[str]) -> List[str]:
        text_aggregate = []

        # Handle Starting Line
        text_start = match.groups()[0]
        if text_start:
            prefix = f"[{idx}]{dl.MULTILINE_START}"
            text = text_start
            text_format = prefix + " " + text
            text_aggregate.append(text_format)

        # Handle Middle Line(s)
        idx, line = next(line_iter)
        while not rx.XML_MULTILINE_END.search(line):
            prefix = f"[{idx}]{dl.MULTILINE_GENERAL}"
            text = line[:-1] if line.endswith("\n") else line  # Strip newline, if exists
            text_format = prefix + " " + text
            text_aggregate.append(text_format)
            try:
                idx, line = next(line_iter)
            except StopIteration:
                return text_aggregate

        # Handle End Line
        match_end = rx.XML_MULTILINE_END.search(line)
        text_end = match_end.groups()[0]
        if text_end:
            prefix = f"[{idx}]{dl.MULTILINE_END}"
            text = text_end
            text_format = prefix + " " + text
            text_aggregate.append(text_format)

        return text_aggregate
