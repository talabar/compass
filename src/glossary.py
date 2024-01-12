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
