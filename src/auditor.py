from enum import Enum
import logging
from pathlib import Path
from typing import List

from ordered_set import OrderedSet

import src.regex as rx
from src.util import get_file_paths

LOGGER = logging.getLogger(__name__)


class FileType(Enum):
    RAW = "RAW"
    TRANSLATE = "TRANSLATE"


class XMLAuditor:
    def __init__(self, dir_base: Path, dir_translate: Path):
        self.files_xml_base: List[Path] = get_file_paths(dir_base, ".xml")
        self.files_xml_translate: List[Path] = get_file_paths(dir_translate, ".xml")

    def audit(self):
        logs: List[str] = []

        for file_raw in self.files_xml_base:
            LOGGER.info(f"|{file_raw.stem}| Auditing...")
            try:
                with open(file_raw, "r", encoding="windows-1251") as fp:
                    content_raw = fp.readlines()
                    ids_base = self.scan(content_raw, FileType.RAW)
            except UnicodeDecodeError as excinfo:
                LOGGER.warning(excinfo.reason)
                continue

            if not ids_base:
                continue

            file_trans = next((x for x in self.files_xml_translate if x.name == file_raw.name), None)
            if not file_trans:
                logs.append(f"{file_raw.name} => (ENTIRE FILE) {str(ids_base.items)}")
                continue

            with open(file_trans, "r", encoding="windows-1251") as fp:
                content_trans = fp.readlines()
                ids_trans = self.scan(content_trans, FileType.TRANSLATE)

            diffs: OrderedSet = ids_base.difference(ids_trans)
            if diffs:
                logs.append(f"{file_raw.name} => {str(diffs.items)}")

        if logs:
            for log in logs:
                LOGGER.info(log)
        else:
            LOGGER.info("Translation Integrity Verified")

    @staticmethod
    def scan(content: List[str], file_type: FileType) -> OrderedSet:
        ids = OrderedSet()

        current_id = None
        for idx, line in enumerate(content, start=1):
            match_id = rx.XML_ID.search(line)
            if match_id:
                current_id = match_id.groups()[0]

            match_simple_text = rx.XML_TEXT_SIMPLE.search(line)
            match_catch_all = rx.XML_CATCH_ALL.search(line)
            match_article = rx.XML_ARTICLE_NAME.search(line)
            match_multiline = rx.XML_TEXT_MULTILINE_START.search(line)

            match = match_simple_text or match_catch_all or match_article or match_multiline

            if match:
                text = match.groups()[0]
                if file_type == FileType.RAW and rx.has_cyrillic(text):
                    ids.add(current_id or idx)
                elif file_type == FileType.TRANSLATE and not rx.has_cyrillic(text):
                    ids.add(current_id)

        return ids
