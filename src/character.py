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