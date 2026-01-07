from enum import Enum

class Race(Enum):
    Drow = 1
    Duegar = 2
    Dwarf = 3
    Elf = 4
    Gnome = 5
    HalfElf = 6
    Halfling = 7
    HalfOrc = 8
    Human = 9
    Svirfneblin = 10


"""
    Requirements listed in lists in this order:
        strength
        intelligence
        wisdom
        dexterity
        constitution
        charisma
"""
race_requirements = {
    Race.Drow: [0,9,0,0,0,0],
    Race.Duegar: [0,9,0,0,9,0],
    Race.Dwarf: [0,0,0,0,9,0],
    Race.Elf: [0,9,0,0,0,0],
    Race.Gnome: [0,9,0,0,9,0],
    Race.HalfElf: [0,0,0,0,9,9],
    Race.Halfling: [0,0,0,9,9,0],
    Race.HalfOrc: [0,0,0,0,0,0],
    Race.Human: [0,0,0,0,0,0],
    Race.Svirfneblin: [0,0,0,0,9,0]
}

def meets_requirements(race, strength, intelligence, wisdom, dexterity, constitution, charisma) -> bool:
    return all(
        race_requirements[race][i] <= stat for i, stat in enumerate([strength, intelligence, wisdom, dexterity, constitution, charisma])
    )