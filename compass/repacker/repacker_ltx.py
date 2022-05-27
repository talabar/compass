import logging

from compass import regex as rx
from compass.datatype import TranslateType
from compass.repacker.repacker_base import BaseRepacker

LOGGER = logging.getLogger(__name__)


class LTXRepacker(BaseRepacker):
    def repack(self):
        LOGGER.info("Repacker LTX Starting...")

        for filename, translate_instr in self.cipher.items():
            if not filename.endswith(".ltx"):
                continue

            contents = self.get_base_contents(filename)

            for line_number, (line_type, text) in translate_instr.items():
                line = contents[line_number - 1]
                if line_type is TranslateType.XML_CATCH_ALL:
                    line_translate = self._text_replace(rx.LTX_INV_NAME, text, line)
                else:
                    raise Exception(
                        "Cipher Error\n"
                        "Invalid Translate Type\n"
                        f"|{filename}| [{line_number}] {line_type}"
                    )

                contents[line_number - 1] = line_translate

            LOGGER.info(f"|{filename}| Saving...")
            self.write_contents(filename, contents)