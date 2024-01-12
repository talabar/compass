from pathlib import Path
from io import TextIOWrapper
from typing import Optional
import sys

from openai import OpenAI

from src.glossary import GLOSSARY, NICKNAMES
from src.util import print_dict_as_prompt


class GPTTranslator:
    def __init__(self, infile: Path, outfile: Path, line_start: int, line_end: Optional[int] = None):
        self.infile = infile
        self.outfile = outfile

        self.client = OpenAI()
        self.cache = {}
        # self.cursor_in: TextIOWrapper = open(self.infile, "r", encoding="windows-1251")
        self.cursor_in: TextIOWrapper = open(self.infile, "r", encoding="utf-8")
        self.cursor_out: TextIOWrapper = open(self.outfile, "a", encoding="utf-8")

        self.static_system_prompt = (
            "Translate Russian to English.\n"
            "Do not include any explanation or justification of the translation.\n"
            "Use an informal tone when the tone is ambiguous.\n"
            "Keep the formatting identical to the prompt.\n"
        )

        self.line_to_process = line_start
        self.line_end = line_end or sys.maxsize

        # Seek to line offset
        print(f"Seeking to LineNo: {line_start}")
        for idx in range(self.line_to_process - 1):
            print(idx)
            self.cursor_in.readline()
        print("Seeking complete.")

    def translate(self):
        line_read = self.cursor_in.readline()
        while line_read and self.line_to_process < self.line_end:
            print(f"Processing LineNo: {self.line_to_process}")
            print(f"RAW: {line_read}")
            if line_read.startswith("FILE"):
                line_write = line_read
                print("Skipping translate...")
                self.cache = {}  # Reset the cache
            elif line_read in self.cache.keys():
                line_write = self.cache[line_read]
                print(f"CACHE: {line_write}")
            else:
                line_write = self._translate_line(line_read)
                self.cache[line_read] = line_write
                print(f"TRANSLATE: {line_write}")

            line_read = self.cursor_in.readline()
            self.line_to_process += 1

            self.cursor_out.writelines(line_write)

        self.cursor_in.close()
        self.cursor_out.close()

    def _translate_line(self, line_raw: str):
        prompt = self._build_prompt(line_raw)
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": line_raw},
            ]
        )
        line_translate = response.choices[0].message.content

        if "\n" in line_translate:
            print("Newline detected in translated line. Stripping the offending char...")
            line_translate = line_translate.replace("\n", "")

        return line_translate + "\n"

    def _build_prompt(self, line: str):
        dynamic_prompt = ""
        if "|" in line:
            dynamic_prompt += "Do not modify strings enclosed in | characters.\n"

        nickname_subset = {key: val for key, val in NICKNAMES.items() if key.casefold() in line.casefold()}
        if nickname_subset:
            dynamic_prompt += print_dict_as_prompt(nickname_subset, "Nicknames: ")

        glossary_subset = {key: val for key, val in GLOSSARY.items() if key.casefold() in line.casefold()}
        if glossary_subset:
            dynamic_prompt += print_dict_as_prompt(glossary_subset, "GLOSSARY: ")

        if dynamic_prompt:
            print("Prompt Edits: " + dynamic_prompt)

        return self.static_system_prompt + dynamic_prompt
