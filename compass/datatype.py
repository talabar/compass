from enum import Enum
from typing import Dict, Tuple


class TranslateType(Enum):
    SIMPLE = "SIMPLE"
    MULTILINE_GENERAL = "MULTILINE_GENERAL"
    MULTILINE_START = "MULTILINE_START"
    MULTILINE_END = "MULTILINE_END"
    PDF_MSG = "PDF_MSG"


Cipher = Dict[str, Dict[int, Tuple[TranslateType, str]]]
