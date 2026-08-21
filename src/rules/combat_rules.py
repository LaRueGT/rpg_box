from enum import StrEnum

from model import pcclass
from rules import dice


def get_attack_values(thaco):
    return THACO_DATA[thaco]

THACO_DATA = {
    20: {-3: 20, -2: 20, -1: 20, 0: 20, 1: 19, 2: 18, 3: 17, 4: 16, 5: 15, 6: 14, 7: 13, 8: 12, 9: 11},
    19: {-3: 20, -2: 20, -1: 20, 0: 19, 1: 18, 2: 17, 3: 16, 4: 15, 5: 14, 6: 13, 7: 12, 8: 11, 9: 10},
    18: {-3: 20, -2: 20, -1: 19, 0: 18, 1: 17, 2: 16, 3: 15, 4: 14, 5: 13, 6: 12, 7: 11, 8: 10, 9: 9},
    17: {-3: 20, -2: 19, -1: 18, 0: 17, 1: 16, 2: 15, 3: 14, 4: 13, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8},
    16: {-3: 19, -2: 18, -1: 17, 0: 16, 1: 15, 2: 14, 3: 13, 4: 12, 5: 11, 6: 10, 7: 9, 8: 8, 9: 7},
    15: {-3: 18, -2: 17, -1: 16, 0: 15, 1: 14, 2: 13, 3: 12, 4: 11, 5: 10, 6: 9, 7: 8, 8: 7, 9: 6},
    14: {-3: 17, -2: 16, -1: 15, 0: 14, 1: 13, 2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7, 8: 6, 9: 5},
    13: {-3: 16, -2: 15, -1: 14, 0: 13, 1: 12, 2: 11, 3: 10, 4: 9, 5: 8, 6: 7, 7: 6, 8: 5, 9: 4},
    12: {-3: 15, -2: 14, -1: 13, 0: 12, 1: 11, 2: 10, 3: 9, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3},
    11: {-3: 14, -2: 13, -1: 12, 0: 11, 1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2},
    10: {-3: 13, -2: 12, -1: 11, 0: 10, 1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 2},
    9: {-3: 12, -2: 11, -1: 10, 0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 2, 9: 2},
    8: {-3: 11, -2: 10, -1: 9, 0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 2, 8: 2, 9: 2},
    7: {-3: 10, -2: 9, -1: 8, 0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2},
    6: {-3: 9, -2: 8, -1: 7, 0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2},
    5: {-3: 8, -2: 7, -1: 6, 0: 5, 1: 4, 2: 3, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2},
}
class SavingThrow(StrEnum):
    DEATH_POISON = "death_poison"
    WANDS = "wands"
    PARALYSIS_PETRIFY = "paralysis_petrify"
    BREATH = "breath"
    SPELLS_RODS_STAVES = "spells_rods_staves"


SAVING_THROW_TYPES = tuple(SavingThrow)

# Rows are ordered by level and columns are D, W, P, B, S.
ACROBAT_SAVING_THROWS = {
    1: (13, 14, 13, 16, 15), 2: (13, 14, 13, 16, 15),
    3: (13, 14, 13, 16, 15), 4: (13, 14, 13, 16, 15),
    5: (12, 13, 11, 14, 13), 6: (12, 13, 11, 14, 13),
    7: (12, 13, 11, 14, 13), 8: (10, 11, 9, 12, 10),
    9: (10, 11, 9, 12, 10), 10: (10, 11, 9, 12, 10),
    11: (10, 11, 9, 12, 10), 12: (10, 11, 9, 12, 10),
    13: (8, 9, 7, 10, 8), 14: (8, 9, 7, 10, 8),
}

ASSASSIN_SAVING_THROWS = ACROBAT_SAVING_THROWS
THIEF_SAVING_THROWS = ACROBAT_SAVING_THROWS

BARBARIAN_SAVING_THROWS = {
    1: (10, 13, 12, 15, 16), 2: (10, 13, 12, 15, 16),
    3: (10, 13, 12, 15, 16), 4: (8, 11, 10, 13, 13),
    5: (8, 11, 10, 13, 13), 6: (8, 11, 10, 13, 13),
    7: (6, 9, 8, 10, 10), 8: (6, 9, 8, 10, 10),
    9: (6, 9, 8, 10, 10), 10: (4, 7, 6, 8, 7),
    11: (4, 7, 6, 8, 7), 12: (4, 7, 6, 8, 7),
    13: (3, 5, 4, 5, 5), 14: (3, 5, 4, 5, 5),
}

BARD_SAVING_THROWS = {
    1: (14, 13, 13, 16, 15), 2: (14, 13, 13, 16, 15),
    3: (14, 13, 13, 16, 15), 4: (14, 13, 13, 16, 15),
    5: (12, 13, 11, 14, 13), 6: (12, 13, 11, 14, 13),
    7: (12, 13, 11, 14, 13), 8: (10, 11, 9, 12, 10),
    9: (10, 11, 9, 12, 10), 10: (10, 11, 9, 12, 10),
    11: (10, 11, 9, 12, 10), 12: (10, 11, 9, 12, 10),
    13: (8, 9, 7, 10, 8), 14: (8, 9, 7, 10, 8),
}

CLERIC_SAVING_THROWS = {
    1: (11, 12, 14, 16, 15), 2: (11, 12, 14, 16, 15),
    3: (11, 12, 14, 16, 15), 4: (11, 12, 14, 16, 15),
    5: (9, 10, 12, 14, 12), 6: (9, 10, 12, 14, 12),
    7: (9, 10, 12, 14, 12), 8: (9, 10, 12, 14, 12),
    9: (6, 7, 9, 11, 9), 10: (6, 7, 9, 11, 9),
    11: (6, 7, 9, 11, 9), 12: (6, 7, 9, 11, 9),
    13: (3, 5, 7, 8, 7), 14: (3, 5, 7, 8, 7),
}

DRUID_SAVING_THROWS = CLERIC_SAVING_THROWS

FIGHTER_SAVING_THROWS = {
    1: (12, 13, 14, 15, 16), 2: (12, 13, 14, 15, 16),
    3: (12, 13, 14, 15, 16), 4: (10, 11, 12, 13, 14),
    5: (10, 11, 12, 13, 14), 6: (10, 11, 12, 13, 14),
    7: (8, 9, 10, 10, 12), 8: (8, 9, 10, 10, 12),
    9: (8, 9, 10, 10, 12), 10: (6, 7, 8, 8, 10),
    11: (6, 7, 8, 8, 10), 12: (6, 7, 8, 8, 10),
    13: (4, 5, 6, 5, 8), 14: (4, 5, 6, 5, 8),
}

KNIGHT_SAVING_THROWS = FIGHTER_SAVING_THROWS
RANGER_SAVING_THROWS = {
    1: (12, 13, 14, 15, 16), 2: (12, 13, 14, 15, 16),
    3: (12, 13, 14, 15, 16), 4: (10, 11, 12, 13, 14),
    5: (10, 11, 12, 13, 14), 6: (10, 11, 12, 13, 14),
    7: (8, 9, 10, 10, 12), 8: (8, 9, 10, 10, 12),
    9: (8, 9, 10, 10, 12), 10: (6, 7, 8, 8, 10),
    11: (6, 7, 8, 8, 10), 12: (6, 7, 8, 8, 10),
    13: (4, 5, 6, 5, 8), 14: (4, 5, 6, 5, 8),
}

ILLUSIONIST_SAVING_THROWS = {
    1: (13, 14, 13, 16, 15), 2: (13, 14, 13, 16, 15),
    3: (13, 14, 13, 16, 15), 4: (13, 14, 13, 16, 15),
    5: (13, 14, 13, 16, 15), 6: (11, 12, 11, 14, 12),
    7: (11, 12, 11, 14, 12), 8: (11, 12, 11, 14, 12),
    9: (11, 12, 11, 14, 12), 10: (11, 12, 11, 14, 12),
    11: (8, 9, 8, 11, 8), 12: (8, 9, 8, 11, 8),
    13: (8, 9, 8, 11, 8), 14: (8, 9, 8, 11, 8),
}

MAGIC_USER_SAVING_THROWS = ILLUSIONIST_SAVING_THROWS

PALADIN_SAVING_THROWS = {
    1: (10, 11, 12, 13, 14), 2: (10, 11, 12, 13, 14),
    3: (10, 11, 12, 13, 14), 4: (8, 9, 10, 11, 12),
    5: (8, 9, 10, 11, 12), 6: (8, 9, 10, 11, 12),
    7: (6, 7, 8, 8, 10), 8: (6, 7, 8, 8, 10),
    9: (6, 7, 8, 8, 10), 10: (4, 5, 6, 6, 8),
    11: (4, 5, 6, 6, 8), 12: (4, 5, 6, 6, 8),
    13: (4, 5, 6, 6, 8), 14: (2, 3, 4, 3, 6),
}

SAVING_THROW_TABLES = {
    pcclass.PCClass.Acrobat: ACROBAT_SAVING_THROWS,
    pcclass.PCClass.Assassin: ASSASSIN_SAVING_THROWS,
    pcclass.PCClass.Barbarian: BARBARIAN_SAVING_THROWS,
    pcclass.PCClass.Bard: BARD_SAVING_THROWS,
    pcclass.PCClass.Cleric: CLERIC_SAVING_THROWS,
    pcclass.PCClass.Druid: DRUID_SAVING_THROWS,
    pcclass.PCClass.Fighter: FIGHTER_SAVING_THROWS,
    pcclass.PCClass.Illusionist: ILLUSIONIST_SAVING_THROWS,
    pcclass.PCClass.Knight: KNIGHT_SAVING_THROWS,
    pcclass.PCClass.MagicUser: MAGIC_USER_SAVING_THROWS,
    pcclass.PCClass.Paladin: PALADIN_SAVING_THROWS,
    pcclass.PCClass.Ranger: RANGER_SAVING_THROWS,
    pcclass.PCClass.Thief: THIEF_SAVING_THROWS,
}


def get_saving_throw_values(class_type, level: int) -> dict[SavingThrow, int]:
    """Return a class's five saving-throw targets for a level."""
    if level < 1:
        raise ValueError("class level must be at least 1")
    table = SAVING_THROW_TABLES[class_type]
    row = table[min(level, max(table))]
    return dict(zip(SAVING_THROW_TYPES, row))


def roll_saving_throw(character, saving_throw: SavingThrow | str) -> bool:
    """Roll 1d20 and succeed when it meets the character's target."""
    key = SavingThrow(saving_throw)
    target = character.saving_throws[key.value]
    if target is None:
        raise ValueError("character has no saving-throw targets")
    return dice.roll(1, 20) >= target
