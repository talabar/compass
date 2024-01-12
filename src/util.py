import os
from pathlib import Path
from typing import List, Optional


def get_file_paths(path: Path, ext: str):
    file_paths: List[Path] = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        file_paths += [
            Path(os.path.join(dirpath, filename))
            for filename in filenames if filename.endswith(ext)
        ]

    return file_paths


def get_file_title(path: Path, root: Path):
    root_suffix = root.parts[-1]
    parts = path.parts
    idx = parts.index(root_suffix)
    parts_sliced = parts[idx:]
    title = os.path.sep.join(parts_sliced)
    return title


def print_dict_as_prompt(dict_raw: dict, prefix: Optional[str] = None):
    prompt: str = prefix
    for key, val in dict_raw.items():
        prompt += f"{key} = {val}, "
    return prompt[:-2] + "\n"
