import random

def roll(num_dice, sides) -> int:
    roll_sum = 0
    for dice_index in range(num_dice):
        roll_sum += random.randint(1, sides)
    return roll_sum
