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
    re.compile(r"мкР[\\/]"): "mcR/",
    re.compile(r"Боеприпасы:"): "Ammunition:",

}

GLOSSARY_MATCH = {
    re.compile(r"А([!\?\.])"): "Ah",
    re.compile(r"Э([!\?\.])"): "Eh",
    re.compile(r"О([!\?\.])"): "Oh",

    # TODO:
    # И? -> And?
    # Delete lines related to Cipher: Currently 7666 - 7707 inclusive
}

DEEPL_ERRORS = {
    re.compile(r"в„–"): "№",
    re.compile(r"[Вв]\S+\s*"): "",
    re.compile(r"Гµ"): "x",
    re.compile(r"Е‚"): "l",
    re.compile(r"Гѕ"): "s",
    re.compile(r"РҐ"): "X",
    re.compile(r"Гј"): "ue",
    re.compile(r"Рњ"): "M",
    re.compile(r"Г©"): "e",
    re.compile(r"UKRAР‡NA"): "UKRAINE",

    # TODO: Make more general catch all for junk characters to straight up delete
    re.compile(r"СЏ\.\.\."): "",
    re.compile(r"РІ\.\.\."): "",

    # re.compile(r'"'): "",
    # r"\s*В[\u0400-\u04FFВ¶®©]*\s*": "",
    # r"Р[^\x00-\x7F]": "Ah",
}

# TODO: Implement this in Repacker 'pre-process'
TRANSLATOR = {
    re.compile(r"Hog"): "Borov",
    re.compile(r"Kishka"): "The Gut",
    re.compile(r"Pussy"): "Gut",
    re.compile(r"Shooter"): "Strelok",
    re.compile(r"[Ss]words?man"): "Marked One",
    re.compile(r"Strelka"): "Strelok",
    re.compile(r"^Download$"): "Load",
    re.compile(r"^Swabbed$"): "Marked One",
    re.compile(r"^Titles$"): "Credits",
}
