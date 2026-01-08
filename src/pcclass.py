from enum import Enum

import race
import alignment

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

def meets_requirements(test_class, test_race, alignment, strength, intelligence, wisdom, dexterity, constitution, charisma) -> bool:
    class_requirements = {
        PCClass.Acrobat: [
            lambda: test_race in [race.Race.Drow, race.Race.Elf, race.Race.HalfElf, race.Race.HalfOrc, race.Race.Human]
        ],
        PCClass.Assassin: [
            lambda: test_race in [race.Race.Drow, race.Race.Duegar, race.Race.Dwarf, race.Race.Elf, race.Race.Gnome, race.Race.HalfElf, race.Race.HalfOrc, race.Race.Human, race.Race.Svirfneblin],
            lambda: alignment != alignment.Alignment.Lawful
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
            lambda: alignment == alignment.Alignment.Neutral,
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