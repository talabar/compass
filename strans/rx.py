import re

XML_SIMPLE = re.compile("<text>(.*)</text>")
XML_MULTILINE_START = re.compile("<text>(.*)")
XML_MULTILINE_END = re.compile(r"(.*)</text>")


def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))
