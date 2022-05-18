from abc import ABC, abstractmethod
import logging
from pathlib import Path
from typing import List, Tuple

from compass import delimiter as dl
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

        return self.line_mapping, self.corpus

    @abstractmethod
    def unpack_file_contents(self, contents: List[str]):
        pass
