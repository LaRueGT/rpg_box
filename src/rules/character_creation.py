from model.character import Character
from model import pcclass
from rules import dice

ABILITY_NAMES = [
    "Strength",
    "Intelligence",
    "Wisdom",
    "Dexterity",
    "Constitution",
    "Charisma",
]

ABILITY_ATTRS = {
    "Strength": "strength",
    "Intelligence": "intelligence",
    "Wisdom": "wisdom",
    "Dexterity": "dexterity",
    "Constitution": "constitution",
    "Charisma": "charisma",
}

SHORT_ABILITY_ATTRS = {
    "str": "strength",
    "int": "intelligence",
    "wis": "wisdom",
    "dex": "dexterity",
    "con": "constitution",
    "cha": "charisma",
}

def roll_base_stats():
    return {
        "str": dice.roll(3, 6),
        "int": dice.roll(3, 6),
        "wis": dice.roll(3, 6),
        "dex": dice.roll(3, 6),
        "con": dice.roll(3, 6),
        "cha": dice.roll(3, 6),
    }

def apply_base_stats(character: Character, base_stats):
    for short_name, attr_name in SHORT_ABILITY_ATTRS.items():
        setattr(character, attr_name, base_stats[short_name])


def apply_race_modifiers(character: Character, base_stats, stat_mods):
    character.strength = base_stats["str"] + stat_mods[0]
    character.intelligence = base_stats["int"] + stat_mods[1]
    character.wisdom = base_stats["wis"] + stat_mods[2]
    character.dexterity = base_stats["dex"] + stat_mods[3]
    character.constitution = base_stats["con"] + stat_mods[4]
    character.charisma = base_stats["cha"] + stat_mods[5]


def build_ability_score_lines(character: Character, base_stats):
    stats = [
        ("Strength", character.strength, base_stats["str"]),
        ("Intelligence", character.intelligence, base_stats["int"]),
        ("Wisdom", character.wisdom, base_stats["wis"]),
        ("Dexterity", character.dexterity, base_stats["dex"]),
        ("Constitution", character.constitution, base_stats["con"]),
        ("Charisma", character.charisma, base_stats["cha"]),
    ]

    lines = ["Roll Ability Scores"]
    for name, current, base in stats:
        color_tag = ""
        end_tag = ""
        if current > base:
            color_tag = "\1green\1"
            end_tag = "\2"
        elif current < base:
            color_tag = "\1red\1"
            end_tag = "\2"
        lines.append(f"{name}: {color_tag}{current}{end_tag}")

    return lines

def get_base_stats(character):
    return {
        "Strength": character.strength,
        "Intelligence": character.intelligence,
        "Wisdom": character.wisdom,
        "Dexterity": character.dexterity,
        "Constitution": character.constitution,
        "Charisma": character.charisma,
    }


def apply_ability_adjustments(character, base_stats, adjustments):
    for ability_name, attr_name in ABILITY_ATTRS.items():
        setattr(
            character,
            attr_name,
            base_stats[ability_name] + adjustments[ability_name],
        )


def build_modifier_lines(character):
    lines = ["Ability Score Modifiers"]

    for ability_name, attr_name in ABILITY_ATTRS.items():
        value = getattr(character, attr_name)
        modifier = character.ability_modifier(value)
        sign = "+" if modifier > 0 else ""
        lines.append(f"{ability_name}: {sign}{modifier}")

    return lines

def calculate_exp_factors(character: Character, selected_classes):
    return [
        pcclass.prime_requisite_factor(
            cls,
            character.strength,
            character.dexterity,
            character.constitution,
            character.intelligence,
            character.wisdom,
            character.charisma,
        )
        for cls in selected_classes
    ]