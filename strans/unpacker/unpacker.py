import logging
from pathlib import Path
from typing import List

from strans.unpacker.unpacker_xml import XMLUnpacker
from strans.util import get_file_paths

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Unpacker:
    def __init__(self, root: Path, file_output: str):
        self.filenames_xml: List[Path] = get_file_paths(root, ".xml")
        self.filenames_ltx: List[Path] = get_file_paths(root, ".ltx")
        self.file_output = file_output

    def unpack(self):
        corpus_unpack = []

        xml_unpacker = XMLUnpacker(self.filenames_xml)
        corpus_unpack += xml_unpacker.unpack()

        with open(self.file_output, "w", encoding="windows-1251") as fp:
            fp.writelines(corpus_unpack)
