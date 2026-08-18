from model.character import Character

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