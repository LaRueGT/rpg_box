import race
import alignment
import pcclass

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

    def ability_modifier(self, ability):
        return (
            -3 if 3 <= ability < 4 else
            -2 if 4 <= ability <= 5 else
            -1 if 6 <= ability <= 8 else
            0 if 9 <= ability <= 12 else
            1 if 13 <= ability <= 15 else
            2 if 16 <= ability <= 17 else
            3 if 17 < ability <= 18 else 0)