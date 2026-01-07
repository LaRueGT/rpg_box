from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton
from direct.showbase.MessengerGlobal import messenger

import diceroll
import character

class Chargen(DirectObject):
    def __init__(self, base, chargen_frame, button_frame):
        super().__init__()
        self.base = base
        self.chargen_frame = chargen_frame
        self.button_frame = button_frame
        self.new_char = character.Character()

    def handle_roll_button(self):
        print("roll button pressed")

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

def roll_abilities():
    print(f"test Strength roll {diceroll.roll(3, 6)}")
    print(f"test Intelligence roll {diceroll.roll(3, 6)}")
    print(f"test Wisdom roll {diceroll.roll(3, 6)}")
    print(f"test Dexterity roll {diceroll.roll(3, 6)}")
    print(f"test Constitution roll {diceroll.roll(3, 6)}")
    print(f"test Charisma roll {diceroll.roll(3, 6)}")