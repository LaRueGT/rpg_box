"""Rules derived from character ability scores."""

from numbers import Integral


def _score(score: int) -> int:
    if isinstance(score, bool) or not isinstance(score, Integral):
        raise TypeError("ability score must be an integer")
    if not 3 <= score <= 18:
        raise ValueError("ability score must be between 3 and 18")
    return score


def ability_modifier(ability_score: int) -> int:
    """Standard modifier for an ability score from 3 through 18."""
    score = _score(ability_score)
    if score == 3:
        return -3
    if score <= 5:
        return -2
    if score <= 8:
        return -1
    if score <= 12:
        return 0
    if score <= 15:
        return 1
    if score <= 17:
        return 2
    return 3


def strength_melee_modifier(strength: int) -> int:
    return ability_modifier(strength)

def strength_open_doors(strength: int) -> int:
    """Target number on 1d6 for forcing open a stuck door."""
    score = _score(strength)
    if score <= 8:
        return 1
    if score <= 12:
        return 2
    if score <= 15:
        return 3
    if score <= 17:
        return 4
    return 5


def intelligence_additional_languages(intelligence: int) -> int:
    score = _score(intelligence)
    if score <= 12:
        return 0
    if score <= 15:
        return 1
    if score <= 17:
        return 2
    return 3


def intelligence_literate(intelligence: int) -> bool:
    return _score(intelligence) >= 6


def intelligence_native_speech(intelligence: int) -> str:
    return "broken" if _score(intelligence) == 3 else "native"


def wisdom_magic_save_modifier(wisdom: int) -> int:
    return ability_modifier(wisdom)


def dexterity_missile_modifier(dexterity: int) -> int:
    return ability_modifier(dexterity)


def dexterity_ac_modifier(dexterity: int) -> int:
    """AC adjustment; positive values lower AC and negative values raise it."""
    return ability_modifier(dexterity)


def dexterity_initiative_modifier(dexterity: int) -> int:
    score = _score(dexterity)
    if score == 3:
        return -2
    if score <= 8:
        return -1
    if score <= 12:
        return 0
    if score <= 17:
        return 1
    return 2


def constitution_hit_point_modifier(constitution: int) -> int:
    return ability_modifier(constitution)


def constitution_hit_points(hit_die_roll: int, constitution: int) -> int:
    """Apply CON to one hit die, never reducing that die below one point."""
    if not isinstance(hit_die_roll, Integral) or hit_die_roll < 0:
        raise ValueError("hit die roll must be a non-negative integer")
    return max(1, hit_die_roll + constitution_hit_point_modifier(constitution))


def charisma_reaction_modifier(charisma: int) -> int:
    score = _score(charisma)
    if score == 3:
        return -2
    if score <= 8:
        return -1
    if score <= 12:
        return 0
    if score <= 17:
        return 1
    return 2


def charisma_max_retainers(charisma: int) -> int:
    score = _score(charisma)
    if score <= 3:
        return 1
    if score <= 5:
        return 2
    if score <= 8:
        return 3
    if score <= 12:
        return 4
    if score <= 15:
        return 5
    if score <= 17:
        return 6
    return 7


def charisma_retainer_loyalty(charisma: int) -> int:
    score = _score(charisma)
    if score <= 3:
        return 4
    if score <= 5:
        return 5
    if score <= 8:
        return 6
    if score <= 12:
        return 7
    if score <= 15:
        return 8
    if score <= 17:
        return 9
    return 10


open_doors = strength_open_doors
additional_languages = intelligence_additional_languages
magic_save_modifier = wisdom_magic_save_modifier
missile_attack_modifier = dexterity_missile_modifier
ac_modifier = dexterity_ac_modifier
initiative_modifier = dexterity_initiative_modifier
hit_point_modifier = constitution_hit_point_modifier
reaction_modifier = charisma_reaction_modifier
max_retainers = charisma_max_retainers
retainer_loyalty = charisma_retainer_loyalty
