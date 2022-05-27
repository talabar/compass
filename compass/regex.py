import re

CIPHER_SCRIPT = re.compile(r"^(\d+)_(\d+)$")
CIPHER_XML_CATCH_ALL = re.compile(r"^(\d+):CA:$")
CIPHER_XML_TEXT_SIMPLE = re.compile(r"^(\d+):SL:$")
CIPHER_XML_TEXT_MULTILINE_GENERAL = re.compile(r"^(\d+):ML:$")
CIPHER_XML_TEXT_MULTILINE_START = re.compile(r"^(\d+):MLS:$")
CIPHER_XML_TEXT_MULTILINE_END = re.compile(r"^(\d+):MLE:$")
CIPHER_XML_PDF_MSG = re.compile(r"^(\d+):PDF:$")

GENERAL_PERCENT_C = re.compile(r"(%c\[.+?])")
GENERAL_PERCENT_C_PADDED = re.compile(r"(\s*%c\[.+?]\s*)")

LTX_INV_NAME = re.compile(r"inv_name(?:_short)?\s*=\s*([^;\n]+)")

SCRIPT_COMMENT = re.compile(r"\s*--|\s*#")
SCRIPT_SIMPLE = re.compile(r'"((?:[^"\\]|\\.)*)"')

XML_CATCH_ALL = re.compile(">(.*)</")
XML_TEXT_SIMPLE = re.compile("<text>(.*)</text>")
XML_TEXT_MULTILINE_START = re.compile("<text>(.*)")
XML_TEXT_MULTILINE_END = re.compile(r"(.*)</text>")


def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))
