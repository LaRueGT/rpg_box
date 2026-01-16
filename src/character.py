import race
import alignment
import pcclass
import diceroll

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

    def ability_modifier(self, ability):
        return (
            -3 if 3 <= ability < 4 else
            -2 if 4 <= ability <= 5 else
            -1 if 6 <= ability <= 8 else
            0 if 9 <= ability <= 12 else
            1 if 13 <= ability <= 15 else
            2 if 16 <= ability <= 17 else
            3 if 17 < ability <= 18 else 0)

    def get_attack_values(self, thaco):
        return THACO_DATA[thaco]

    def roll_hp(self):
        num_classes = len(self.char_classes)
        for charclass in self.char_classes:
            quantity, size = pcclass.get_hit_die(charclass, self.level)
            total = 0
            for _ in range(quantity):
                die_roll = diceroll.roll(1, size)
                # Reroll 1s once if level is 3 or less
                if self.level <= 3 and die_roll == 1:
                    die_roll = diceroll.roll(1, size)
                total += die_roll
            # Divide total by number of classes
            share = total / num_classes
            self.max_hp += int(share)
            self.hp_fraction += share - int(share)
            # If fractions add up to nearly 1 (using 0.9 as a safe threshold for floating point)
            if self.hp_fraction >= 0.9:
                self.max_hp += 1
                self.hp_fraction = 0

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