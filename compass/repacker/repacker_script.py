import logging

from compass import regex as rx
from compass.datatype import TranslateType
from compass.repacker.repacker_base import BaseRepacker

LOGGER = logging.getLogger(__name__)


class ScriptRepacker(BaseRepacker):
    def repack(self):
        LOGGER.info("Repacker Script Starting...")

        for filename, translate_instr in self.cipher.items():
            if not filename.endswith(".script"):
                continue

            contents = self.get_base_contents(filename)

            for line_number, (match_number, text) in translate_instr.items():
                line = contents[line_number - 1]
                # TODO: Flesh out once Script Cipher construction is confirmed working
                pass
