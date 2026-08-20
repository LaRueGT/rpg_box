from model import pcclass
from model.character import Character
from rules import dice

def roll_hp_for_character(character: Character) -> None:
    num_classes = len(character.char_classes)
    if num_classes == 0:
        return
    total = 0
    for class_index, charclass in enumerate(character.char_classes):
        # Characters created before per-class levels were initialized may
        # still have fewer level entries than selected classes.  Treat those
        # missing entries as first-level classes.
        class_level = character.level[class_index] if class_index < len(character.level) else 1
        quantity, size = pcclass.get_hit_die(charclass, class_level)
        for _ in range(quantity):
            die_roll = dice.roll(1, size)
            # Reroll 1s once if level is 3 or less.
            if class_level <= 3 and die_roll == 1:
                die_roll = dice.roll(1, size)
            total += die_roll

    # Constitution modifies the combined pool once before it is averaged
    # across the character's classes.
    total += character.ability_modifier(character.constitution)

    # Divide the final pool by the number of classes.
    share = total / num_classes
    character.max_hp += int(share)
    character.hp_fraction += share - int(share)
    # If fractions add up to nearly 1.
    if character.hp_fraction >= 0.9:
        character.max_hp += 1
        character.hp_fraction = 0

    # A character must always start with at least 1 hit point, even after
    # a poor roll and a Constitution penalty.
    if character.max_hp + character.hp_fraction < 1:
        character.max_hp = 1
        character.hp_fraction = 0
