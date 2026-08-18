from enum import Enum

from model import race, alignment

class PCClass(Enum):
    Acrobat = 1
    Assassin = 2
    Barbarian = 3
    Bard = 4
    Cleric = 5
    Druid = 6
    Fighter = 7
    Illusionist = 8
    Knight = 9
    MagicUser = 10
    Paladin = 11
    Ranger = 12
    Thief = 13

    def __str__(self):
        if self.name == "MagicUser":
            return "Magic-User"
        return self.name

"""
    Requirements listed in lists in this order:
        strength
        intelligence
        wisdom
        dexterity
        constitution
        charisma
"""

def meets_requirements(test_class, test_race, test_alignment, strength, intelligence, wisdom, dexterity, constitution, charisma) -> bool:
    class_requirements = {
        PCClass.Acrobat: [
            lambda: test_race in [race.Race.Drow, race.Race.Elf, race.Race.HalfElf, race.Race.HalfOrc, race.Race.Human]
        ],
        PCClass.Assassin: [
            lambda: test_race in [race.Race.Drow, race.Race.Duegar, race.Race.Dwarf, race.Race.Elf, race.Race.Gnome, race.Race.HalfElf, race.Race.HalfOrc, race.Race.Human, race.Race.Svirfneblin],
            lambda: test_alignment != alignment.Alignment.Lawful
        ],
        PCClass.Barbarian: [
            lambda: dexterity >= 9,
            lambda: test_race in [race.Race.Human],
        ],
        PCClass.Bard: [
            lambda: dexterity >= 9,
            lambda: intelligence >= 9,
            lambda: test_race in [race.Race.HalfElf, race.Race.Human]
        ],
        PCClass.Cleric: [
            lambda: test_race in [race.Race.Drow, race.Race.Duegar, race.Race.Dwarf, race.Race.Elf, race.Race.Gnome, race.Race.HalfElf, race.Race.HalfOrc, race.Race.Human, race.Race.Svirfneblin]
        ],
        PCClass.Druid: [
            lambda: test_alignment == alignment.Alignment.Neutral,
            lambda: test_race in [race.Race.Elf, race.Race.HalfElf, race.Race.Halfling, race.Race.Human]
        ],
        PCClass.Fighter: [
            lambda: True
        ],
        PCClass.Illusionist: [
            lambda: dexterity >= 9,
            lambda: test_race in [race.Race.Gnome, race.Race.Human, race.Race.Svirfneblin]
        ],
        PCClass.Knight: [
            lambda: dexterity >= 9,
            lambda: constitution >= 9,
            lambda: test_race in [race.Race.Drow, race.Race.Elf, race.Race.HalfElf, race.Race.Human]
        ],
        PCClass.MagicUser: [
            lambda: test_race in [race.Race.Drow, race.Race.Elf, race.Race.HalfElf, race.Race.Human]
        ],
        PCClass.Paladin: [
            lambda: charisma >= 9,
            lambda: test_race in [race.Race.HalfElf, race.Race.Human]
        ],
        PCClass.Ranger: [
            lambda: constitution >= 9,
            lambda: wisdom >= 9,
            lambda: test_race in [race.Race.Drow, race.Race.Elf, race.Race.HalfElf, race.Race.Human]
        ],
        PCClass.Thief: [
            lambda: True
        ],
    }
    result = all(condition() for condition in class_requirements[test_class])
    return result

def get_hit_die(test_class, level) -> tuple[int, int]:
    match test_class:
        case PCClass.Acrobat:
            return 1, 4
        case PCClass.Assassin:
            return 1, 4
        case PCClass.Barbarian:
            return 1, 8
        case PCClass.Bard:
            return 1, 6
        case PCClass.Cleric:
            return 1, 6
        case PCClass.Druid:
            return 1, 6
        case PCClass.Fighter:
            return 1, 8
        case PCClass.Illusionist:
            return 1, 4
        case PCClass.Knight:
            return 1, 8
        case PCClass.MagicUser:
            return 1, 4
        case PCClass.Paladin:
            return 1, 8
        case PCClass.Ranger:
            return 1, 8
        case PCClass.Thief:
            return 1, 4
        case _:
            return 1, 4

def prime_requisite_factor(test_class, strength, dexterity, constitution, intelligence, wisdom, charisma) -> float:
    match test_class:
        case PCClass.Acrobat:
            return (
                0.8 if 3<= dexterity <= 5 else
                0.9 if 6 <= dexterity <= 8 else
                1 if 9 <= dexterity <=12 else
                1.05 if 15 <= dexterity <= 15 else
                1.1 if 16 <= dexterity <= 18 else 1)
        case PCClass.Assassin:
            return (
                0.8 if 3 <= dexterity <= 5 else
                0.9 if 6 <= dexterity <= 8 else
                1 if 9 <= dexterity <= 12 else
                1.05 if 15 <= dexterity <= 15 else
                1.1 if 16 <= dexterity <= 18 else 1)
        case PCClass.Barbarian:
            if strength >= 16 and constitution >= 16:
                return 1.1
            elif strength >= 13 or constitution >= 13:
                return 1.05
            else:
                return 1
        case PCClass.Bard:
            return (
                0.8 if 3 <= charisma <= 5 else
                0.9 if 6 <= charisma <= 8 else
                1 if 9 <= charisma <= 12 else
                1.05 if 15 <= charisma <= 15 else
                1.1 if 16 <= charisma <= 18 else 1)
        case PCClass.Cleric:
            return (
                0.8 if 3 <= wisdom <= 5 else
                0.9 if 6 <= wisdom <= 8 else
                1 if 9 <= wisdom <= 12 else
                1.05 if 15 <= wisdom <= 15 else
                1.1 if 16 <= wisdom <= 18 else 1)
        case PCClass.Druid:
            return (
                0.8 if 3 <= wisdom <= 5 else
                0.9 if 6 <= wisdom <= 8 else
                1 if 9 <= wisdom <= 12 else
                1.05 if 15 <= wisdom <= 15 else
                1.1 if 16 <= wisdom <= 18 else 1)
        case PCClass.Fighter:
            return (
                0.8 if 3 <= strength <= 5 else
                0.9 if 6 <= strength <= 8 else
                1 if 9 <= strength <= 12 else
                1.05 if 15 <= strength <= 15 else
                1.1 if 16 <= strength <= 18 else 1)
        case PCClass.Illusionist:
            return (
                0.8 if 3 <= intelligence <= 5 else
                0.9 if 6 <= intelligence <= 8 else
                1 if 9 <= intelligence <= 12 else
                1.05 if 15 <= intelligence <= 15 else
                1.1 if 16 <= intelligence <= 18 else 1)
        case PCClass.Knight:
            return (
                0.8 if 3 <= strength <= 5 else
                0.9 if 6 <= strength <= 8 else
                1 if 9 <= strength <= 12 else
                1.05 if 15 <= strength <= 15 else
                1.1 if 16 <= strength <= 18 else 1)
        case PCClass.MagicUser:
            return (
                0.8 if 3 <= intelligence <= 5 else
                0.9 if 6 <= intelligence <= 8 else
                1 if 9 <= intelligence <= 12 else
                1.05 if 15 <= intelligence <= 15 else
                1.1 if 16 <= intelligence <= 18 else 1)
        case PCClass.Paladin:
            if strength >= 16 and wisdom >= 16:
                return 1.1
            elif strength >= 13 or wisdom >= 13:
                return 1.05
            else:
                return 1
        case PCClass.Ranger:
            return (
                0.8 if 3 <= strength <= 5 else
                0.9 if 6 <= strength <= 8 else
                1 if 9 <= strength <= 12 else
                1.05 if 15 <= strength <= 15 else
                1.1 if 16 <= strength <= 18 else 1)
        case PCClass.Thief:
            return (
                0.8 if 3 <= dexterity <= 5 else
                0.9 if 6 <= dexterity <= 8 else
                1 if 9 <= dexterity <= 12 else
                1.05 if 15 <= dexterity <= 15 else
                1.1 if 16 <= dexterity <= 18 else 1)
        case _:
            return 1

def is_prime_requisite(test_class, stat) -> bool:
    match test_class:
        case PCClass.Acrobat:
            return stat in 'dexterity'
        case PCClass.Assassin:
            return stat in 'dexterity'
        case PCClass.Barbarian:
            return stat in 'strength' or stat in 'constitution'
        case PCClass.Bard:
            return stat in 'charisma'
        case PCClass.Cleric:
            return stat in 'wisdom'
        case PCClass.Druid:
            return stat in 'wisdom'
        case PCClass.Fighter:
            return stat in 'strength'
        case PCClass.Illusionist:
            return stat in 'intelligence'
        case PCClass.Knight:
            return stat in 'strength'
        case PCClass.MagicUser:
            return stat in 'intelligence'
        case PCClass.Paladin:
            return stat in 'strength' or stat in 'wisdom'
        case PCClass.Ranger:
            return stat in 'strength'
        case PCClass.Thief:
            return stat in 'dexterity'
        case _:
            return False

def can_reduce(test_classes, stat) -> bool:
    if not set(test_classes).isdisjoint([PCClass.Acrobat, PCClass.Assassin, PCClass.Thief]) and stat == 'strength':
        return False
    else:
        return True