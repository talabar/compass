import logging

from compass import regex as rx
from compass.datatype import TranslateType
from compass.repacker.repacker_base import BaseRepacker

LOGGER = logging.getLogger(__name__)


class XMLRepacker(BaseRepacker):
    def repack(self):
        LOGGER.info("Starting...")

        for filename, translate_instr in self.cipher.items():
            if not filename.endswith(".xml"):
                continue

            contents = self.get_base_contents(filename)

            for line_number, (line_type, text) in translate_instr.items():
                line = contents[line_number - 1]
                if line_type is TranslateType.SIMPLE:
                    line_translate = self._text_replace(rx.XML_SIMPLE, text, line)
                elif line_type is TranslateType.MULTILINE_GENERAL:
                    line_translate = text
                elif line_type is TranslateType.MULTILINE_START:
                    line_translate = self._text_replace(rx.XML_MULTILINE_START, text, line)
                elif line_type is TranslateType.MULTILINE_END:
                    line_translate = self._text_replace(rx.XML_MULTILINE_END, text, line)
                else:
                    raise Exception(
                        "Cipher Error\n"
                        "Invalid Translate Type\n"
                        f"|{filename}| [{line_number}] {line_type}"
                    )

                contents[line_number - 1] = line_translate

            LOGGER.info(f"|{filename}| Saving...")
            self.write_contents(filename, contents)
