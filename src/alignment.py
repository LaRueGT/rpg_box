from enum import Enum

class Alignment(Enum):
    Lawful = 1
    Neutral = 2
    Chaotic = 3

    def __str__(self):
        return self.name
