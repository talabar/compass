import re

CIPHER_LTX_INV_NAME = re.compile(r"^(\d+):LIN:$")
CIPHER_SCRIPT = re.compile(r"^(\d+)_(\d+)$")
CIPHER_XML_ARTICLE_NAME = re.compile(r"^(\d+):XAN:$")
CIPHER_XML_CATCH_ALL = re.compile(r"^(\d+):XCA:$")
CIPHER_XML_TEXT_SIMPLE = re.compile(r"^(\d+):XSL:$")
CIPHER_XML_TEXT_MULTILINE_GENERAL = re.compile(r"^(\d+):XML:$")
CIPHER_XML_TEXT_MULTILINE_START = re.compile(r"^(\d+):XMLS:$")
CIPHER_XML_TEXT_MULTILINE_END = re.compile(r"^(\d+):XMLE:$")

GENERAL_PERCENT_C = re.compile(r"(%c\[.+?])")
GENERAL_PERCENT_C_PADDED = re.compile(r"(\s*%c\[.+?]\s*)")

LTX_INV_NAME = re.compile(r"inv_name(?:_short)?\s*=\s*([^;\n]+)")

SCRIPT_COMMENT = re.compile(r"\s*--|\s*#")
SCRIPT_DBG = re.compile(r"~C0C|\[~T|#DBG")
SCRIPT_SIMPLE = re.compile(r'"((?:[^"\\]|\\.)*)"')

XML_ID = re.compile(r"id=\"(.+?)\"")
XML_ARTICLE_NAME = re.compile(r"<article\s.+?name=\"(.+?)\".*?>")
XML_CATCH_ALL = re.compile(r">(.*)</")
XML_TEXT_SIMPLE = re.compile(r"<text>(.*)</text>")
XML_TEXT_MULTILINE_START = re.compile(r"<text>(.*)")
XML_TEXT_MULTILINE_END = re.compile(r"(.*)</text>")


def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))
