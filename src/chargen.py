from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton
from direct.showbase.MessengerGlobal import messenger

import diceroll
import character

class Chargen(DirectObject):
    def __init__(self, base, ability_label, button_frame):
        super().__init__()
        self.base = base
        self.ability_label = ability_label
        self.button_frame = button_frame
        self.new_char = character.Character()

    def handle_roll_button(self):
        print("roll button pressed")
        self.new_char.strength = diceroll.roll(3, 6)
        print(f"Strength roll total = {self.new_char.strength}!")
        self.new_char.intelligence = diceroll.roll(3, 6)
        print(f"Intelligence roll total = {self.new_char.intelligence}!")
        self.new_char.wisdom = diceroll.roll(3, 6)
        print(f"Wisdom roll total = {self.new_char.wisdom}!")
        self.new_char.dexterity = diceroll.roll(3, 6)
        print(f"Dexterity roll total = {self.new_char.dexterity}!")
        self.new_char.constitution = diceroll.roll(3, 6)
        print(f"Constitution roll total = {self.new_char.constitution}!")
        self.new_char.charisma = diceroll.roll(3, 6)
        print(f"Charisma roll total = {self.new_char.charisma}!")
        self.ability_label.setText(f"Roll Ability Scores\nStrength:\t\t{self.new_char.strength}\nIntelligence:\t\t{self.new_char.intelligence}\nWisdom:\t\t{self.new_char.wisdom}\nDexterity:\t\t{self.new_char.dexterity}\nConstitution:\t{self.new_char.constitution}\nCharisma:\t\t{self.new_char.charisma}",)

    def handle_done_button(self):
        print("done button pressed")
        messenger.send("chargen_finished")

    def handle_exit_button(self):
        print("exit button pressed")
        messenger.send("chargen_finished")

    def display_chargen_buttons(self):
        roll_button = DirectButton(parent=self.button_frame, text="Roll Stats", scale=.05, command=self.handle_roll_button)
        done_button = DirectButton(parent=self.button_frame, text="Done", scale=.05, command=self.handle_done_button)
        exit_button = DirectButton(parent=self.button_frame, text="Exit", scale=.05, command=self.handle_exit_button)
        self.button_frame.addItem(roll_button)
        self.button_frame.addItem(done_button)
        self.button_frame.addItem(exit_button)
