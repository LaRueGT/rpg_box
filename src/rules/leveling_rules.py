from model import pcclass
from model.character import Character
from rules import dice
from rules.ability_rules import constitution_hit_points
from rules.combat_rules import SAVING_THROW_TYPES, get_saving_throw_values


def update_saving_throws(character: Character) -> dict[str, int | None]:
    """Recalculate saving throws after class or class-level changes.

    Multiclass characters use the lowest (best) target independently for
    each saving-throw category.
    """
    if not character.char_classes:
        character.saving_throws = {save.value: None for save in SAVING_THROW_TYPES}
        return character.saving_throws

    class_rows = []
    for class_index, charclass in enumerate(character.char_classes):
        class_level = character.level[class_index] if class_index < len(character.level) else 1
        class_rows.append(get_saving_throw_values(charclass, class_level))

    character.saving_throws = {
        save.value: min(row[save] for row in class_rows)
        for save in SAVING_THROW_TYPES
    }
    return character.saving_throws


def set_class_level(character: Character, class_index: int, level: int) -> None:
    """Set one class level and refresh the character's saving throws."""
    if class_index < 0 or class_index >= len(character.char_classes):
        raise IndexError("class index is out of range")
    if level < 1:
        raise ValueError("class level must be at least 1")
    while len(character.level) < len(character.char_classes):
        character.level.append(1)
    character.level[class_index] = level
    update_saving_throws(character)

def roll_hp_for_character(character: Character) -> None:
    update_saving_throws(character)
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
            total += constitution_hit_points(die_roll, character.constitution)

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
