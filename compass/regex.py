import re

CIPHER_SIMPLE = re.compile(r"^(\d+)$")
CIPHER_MULTILINE_GENERAL = re.compile(r"^(\d+):ML:$")
CIPHER_MULTILINE_START = re.compile(r"^(\d+):MLS:$")
CIPHER_MULTILINE_END = re.compile(r"^(\d+):MLE:$")
CIPHER_PDF_MSG = re.compile(r"^(\d+):PDF:$")

LTX_INV_NAME = re.compile(r"inv_name(?:_short)?\s*=\s*([^;\n]+)")

XML_SIMPLE = re.compile("<text>(.*)</text>")
XML_MULTILINE_START = re.compile("<text>(.*)")
XML_MULTILINE_END = re.compile(r"(.*)</text>")
XML_PDF_MSG = re.compile(r"\s*<string id=\".+\">(.+)</string>")


def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))
