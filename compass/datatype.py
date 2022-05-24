from enum import Enum
from typing import Dict, Tuple, Union


class TranslateType(Enum):
    SIMPLE = "SIMPLE"
    MULTILINE_GENERAL = "MULTILINE_GENERAL"
    MULTILINE_START = "MULTILINE_START"
    MULTILINE_END = "MULTILINE_END"
    PDF_MSG = "PDF_MSG"
    SCRIPT = "SCRIPT"


Instr_Script = Dict[int, str]
# Cipher = Dict[str, Dict[int, Tuple[TranslateType, str]]]
Cipher = Dict[str, Dict[int, Tuple[TranslateType, Union[str, Instr_Script]]]]
