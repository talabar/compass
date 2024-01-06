from abc import ABC, abstractmethod
import logging
from pathlib import Path
import re
from typing import List, Tuple

from compass import delimiter as dl
from compass import regex as rx
from compass.glossary import GLOSSARY, GLOSSARY_MATCH
from compass.util import get_file_title

LOGGER = logging.getLogger(__name__)


class BaseUnpacker(ABC):
    def __init__(self, root: Path):
        self.root = root
        self.stem = None
        self.line_mapping = []
        self.corpus = []

        # Set by Subclass
        self.filenames = []

    def unpack(self) -> Tuple[List[str], List[str]]:
        LOGGER.info(f"{self.__class__.__name__} Starting...")

        for filename in self.filenames:

            self.stem = filename.stem

            LOGGER.debug(f"|{filename.parts[-1]}| Processing...")

            with open(filename, "r", encoding="windows-1251", errors="ignore") as input_fp:
                file_contents = input_fp.readlines()

            file_title = dl.FILE + " " + get_file_title(filename, self.root) + "\n"
            self.line_mapping.append(file_title)
            self.corpus.append(file_title)

            self.unpack_file_contents(file_contents)

            if self.line_mapping[-1] == file_title:
                self.line_mapping.pop()
                self.corpus.pop()
            else:
                LOGGER.info(f"|{filename.parts[-1]}| Unpacked Successfully")

        self.post_process()
        return self.line_mapping, self.corpus

    @abstractmethod
    def unpack_file_contents(self, contents: List[str]):
        pass

    def post_process(self):
        for idx, text in enumerate(self.corpus):
            self.corpus[idx] = self.corpus[idx].replace("\\\\n", dl.NEWLINE_ESCAPE)
            # Condition needed to avoid mistaking newlines for file paths (i.e. kotovod\new_compass.script)
            if not self.corpus[idx].startswith("FILE"):
                self.corpus[idx] = self.corpus[idx].replace("\\n", dl.NEWLINE)

            self.corpus[idx] = self.corpus[idx].replace("\\\"", dl.QUOTATION_ESCAPE)
            self.corpus[idx] = self.corpus[idx].replace("\"", dl.QUOTATION)

            # A guillemet is a type of quotation used in various languages (including russian)
            # Translation engines often replace these with quotes, and it is difficult to stop that behavior
            # Important to include these as to not break scripting (that uses regular quotes as part of the code)
            self.corpus[idx] = self.corpus[idx].replace("«", dl.GUILLEMET_LEFT)
            self.corpus[idx] = self.corpus[idx].replace("»", dl.GUILLEMET_RIGHT)
