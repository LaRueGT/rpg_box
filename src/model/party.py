from model import race, alignment, pcclass, character
from rules import dice

class Party:
    def __init__(self):
        self.name = ""
        self.members:list[character.Character] = []

    def add_member(self, member:character.Character):
        if member not in self.members:
            self.members.append(member)
            self.size += 1

    @property
    def size(self):
        return len(self.members)

    def remove_member(self, member:character.Character):
        if member in self.members:
            self.members.remove(member)
            self.size -= 1
