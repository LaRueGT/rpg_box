from model import race, alignment, pcclass
from rules import dice

class Character:
    def __init__(self):
        self.strength = 0
        self.intelligence = 0
        self.wisdom = 0
        self.dexterity = 0
        self.constitution = 0
        self.charisma = 0
        self.char_race = None
        self.gender = None
        self.char_classes = []
        self.exp_factor = []
        self.level = 1
        self.exp_amount = []
        self.char_alignment = None
        self.thaco = 19
        self.attack_values = {}
        self.max_hp = 0
        self.hp_fraction = 0
        self.name = ""

    def ability_modifier(self, ability_value):
        return (
            -3 if 3 <= ability_value < 4 else
            -2 if 4 <= ability_value <= 5 else
            -1 if 6 <= ability_value <= 8 else
            0 if 9 <= ability_value <= 12 else
            1 if 13 <= ability_value <= 15 else
            2 if 16 <= ability_value <= 17 else
            3 if 17 < ability_value <= 18 else 0)
