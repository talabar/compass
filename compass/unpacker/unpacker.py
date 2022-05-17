import logging
from pathlib import Path
from typing import List

from compass.unpacker.unpacker_ltx import LTXUnpacker
from compass.unpacker.unpacker_xml import XMLUnpacker
from compass.util import get_file_paths

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Unpacker:
    def __init__(self, root: Path, output_stem: str):
        self.filenames_xml: List[Path] = get_file_paths(root, ".xml")
        self.filenames_ltx: List[Path] = get_file_paths(root, ".ltx")
        self.filename_mapping = output_stem + "_mapping.txt"
        self.filename_corpus = output_stem + "_corpus.txt"

    def unpack(self):
        xml_unpacker = XMLUnpacker(self.filenames_xml)
        mapping_xml, corpus_xml = xml_unpacker.unpack()

        ltx_unpacker = LTXUnpacker(self.filenames_ltx)
        mapping_ltx, corpus_ltx = ltx_unpacker.unpack()

        mapping = mapping_xml + mapping_ltx
        corpus = corpus_xml + corpus_ltx

        with open(self.filename_mapping, "w+", encoding="windows-1251") as fp:
            fp.writelines(mapping)

        with open(self.filename_corpus, "w+", encoding="windows-1251") as fp:
            fp.writelines(corpus)
