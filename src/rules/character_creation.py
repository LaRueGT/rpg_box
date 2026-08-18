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

def roll_base_stats():
    return {ability_name: dice.roll(3, 6) for ability_name in ABILITY_NAMES}

def apply_base_stats(character: Character, base_stats):
    for ability_name, attr_name in ABILITY_ATTRS.items():
        setattr(character, attr_name, base_stats[ability_name])

def apply_race_modifiers(character: Character, base_stats, stat_mods):
    for ability_name, modifier in zip(ABILITY_NAMES, stat_mods):
        attr_name = ABILITY_ATTRS[ability_name]
        setattr(character, attr_name, base_stats[ability_name] + modifier)

def build_ability_score_lines(character: Character, base_stats):
    lines = ["Roll Ability Scores"]
    for ability_name, attr_name in ABILITY_ATTRS.items():
        current = getattr(character, attr_name)
        base = base_stats[ability_name]
        color_tag = ""
        end_tag = ""
        if current > base:
            color_tag = "\1green\1"
            end_tag = "\2"
        elif current < base:
            color_tag = "\1red\1"
            end_tag = "\2"
        lines.append(f"{ability_name}: {color_tag}{current}{end_tag}")
    return lines

def get_base_stats(character: Character):
    return {
        ability_name: getattr(character, attr_name)
        for ability_name, attr_name in ABILITY_ATTRS.items()
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