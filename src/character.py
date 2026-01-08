import race
import alignment

class Character:
    def __init__(self):
        self.strength = 0
        self.intelligence = 0
        self.wisdom = 0
        self.dexterity = 0
        self.constitution = 0
        self.charisma = 0
        self.char_race = race.Race.Human
        self.char_alignment = alignment.Alignment.Neutral