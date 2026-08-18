from model import race, alignment, pcclass, character
from rules import diceroll

class Party:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.members:list[character.Character] = []

    def add_member(self, member:character.Character):
        if member not in self.members:
            self.members.append(member)
            self.size += 1

    def remove_member(self, member:character.Character):
        if member in self.members:
            self.members.remove(member)
            self.size -= 1
