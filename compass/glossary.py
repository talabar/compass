import re

GLOSSARY = {
    re.compile(r"Призрака"): "Ghost",
    re.compile(r"Стрелка"): "Strelok",
    re.compile(r"Долг"): "Duty",
    re.compile(r"Свобода"): "Freedom",
    re.compile(r"Кишке"): "Gut",
    re.compile(r"Меченный"): "Marked One",
    re.compile(r"ПДА"): "PDA",
    re.compile(r"выброса"): "emission",
    re.compile("выброс"): "blowout",
    re.compile(r"Мозговыжигатель"): "Brain Scorcher",
    re.compile(r"мкР[\\/]"): "mcR/"
}

GLOSSARY_MATCH = {
    re.compile(r"А([!\?\.])"): "Ah",
    re.compile(r"Э([!\?\.])"): "Eh",
    re.compile(r"О([!\?\.])"): "Oh",
}

DEEPL_ERRORS = {
    re.compile(r"в„–"): "№",
    re.compile(r"[Вв]\S+\s*"): "",
    re.compile(r'"'): "",
    re.compile(r"Гµ"): "x",
    re.compile(r"Е‚"): "l",
    re.compile(r"Гѕ"): "s",
    # r"\s*В[\u0400-\u04FFВ¶®©]*\s*": "",
    # r"Р[^\x00-\x7F]": "Ah",
}
