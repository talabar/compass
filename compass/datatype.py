from enum import Enum
from typing import Dict, Tuple, Union


class TranslateType(Enum):
    LTX_INV_NAME = "LTX_INV_NAME"
    SCRIPT = "SCRIPT"
    XML_CATCH_ALL = "XML_CATCH_ALL"
    XML_TEXT_SIMPLE = "XML_TEXT_SIMPLE"
    XML_TEXT_MULTILINE_GENERAL = "XML_TEXT_MULTILINE_GENERAL"
    XML_TEXT_MULTILINE_START = "XML_TEXT_MULTILINE_START"
    XML_TEXT_MULTILINE_END = "XML_TEXT_MULTILINE_END"


Instr_Script = Dict[int, str]
Cipher = Dict[str, Dict[int, Tuple[TranslateType, Union[str, Instr_Script]]]]
