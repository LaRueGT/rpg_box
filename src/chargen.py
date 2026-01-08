import alignment
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton, DGG
from panda3d.core import TextNode, NodePath
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.showbase.MessengerGlobal import messenger

import diceroll
import character
import race

class Chargen(DirectObject):
    def __init__(self, base, ability_label, racelist_frame, alignment_frame, button_frame):
        super().__init__()
        self.base = base
        self.ability_label = ability_label
        self.race_list_frame = racelist_frame
        self.alignment_frame = alignment_frame
        self.button_frame = button_frame
        self.roll_button = NodePath()
        self.label_font = self.base.loader.loadFont('../fonts/EBGaramond-VariableFont_wght.ttf')
        self.races = []
        self.race_buttons = []
        self.selected_race = [None]
        self.alignments = []
        self.alignment_buttons = []
        self.selected_alignment = [None]
        self.new_char = character.Character()

    def handle_roll_button(self):
        print("roll button pressed")
        self.roll_button['state'] = DGG.DISABLED
        self.new_char.strength = diceroll.roll(3, 6)
        self.new_char.intelligence = diceroll.roll(3, 6)
        self.new_char.wisdom = diceroll.roll(3, 6)
        self.new_char.dexterity = diceroll.roll(3, 6)
        self.new_char.constitution = diceroll.roll(3, 6)
        self.new_char.charisma = diceroll.roll(3, 6)
        self.ability_label.setText(f"Roll Ability Scores\nStrength:\t\t{self.new_char.strength}\nIntelligence:\t\t{self.new_char.intelligence}\nWisdom:\t\t{self.new_char.wisdom}\nDexterity:\t\t{self.new_char.dexterity}\nConstitution:\t{self.new_char.constitution}\nCharisma:\t\t{self.new_char.charisma}",)
        for race_index in range(len(self.races)):
            if race.meets_requirements(self.races[race_index], self.new_char.strength, self.new_char.intelligence, self.new_char.wisdom, self.new_char.dexterity, self.new_char.constitution, self.new_char.charisma):
                self.race_buttons[race_index]['state'] = DGG.NORMAL
        for btn in self.alignment_buttons:
            btn['state'] = DGG.NORMAL

    def handle_race_button(self, race_index):
        self.new_char.char_race = self.races[race_index]
        print(f"Selected race: {self.new_char.char_race.name}")

    def handle_alignment_button(self, align_index):
        self.new_char.char_alignment = self.alignments[align_index]
        print(f"Selected alignemnt: {self.new_char.char_alignment.name}")

    def handle_done_button(self):
        print("done button pressed")
        messenger.send("chargen_finished")

    def handle_exit_button(self):
        print("exit button pressed")
        messenger.send("chargen_finished")

    def display_chargen_buttons(self):
        self.roll_button = DirectButton(
            parent=self.button_frame,
            text="Roll Stats",
            scale=.05,
            command=self.handle_roll_button,
            text_fg=(0, 0, 0, 1),
            text3_fg=(0.6, 0.6, 0.6, 1)  # Color for state 3 (Disabled)
        )
        done_button = DirectButton(parent=self.button_frame, text="Done", scale=.05, command=self.handle_done_button)
        exit_button = DirectButton(parent=self.button_frame, text="Exit", scale=.05, command=self.handle_exit_button)
        self.button_frame.addItem(self.roll_button)
        self.button_frame.addItem(done_button)
        self.button_frame.addItem(exit_button)

    def display_race_picker(self):
        self.race_buttons = []
        for race_index, race_option in enumerate(race.Race):
            self.races.append(race_option)
            btn = DirectRadioButton(parent=self.race_list_frame,
                                    text=str(race_option),
                                    scale=0.07,
                                    pos=(0.1, 0, -0.05 - (race_index * 0.1)),
                                    frameSize=(0, 10, -0.5, 1),
                                    text_pos=(1.2, 0),
                                    variable=self.selected_race,
                                    value=[race_option.value],
                                    others=self.race_buttons,
                                    text_font=self.label_font,
                                    text_align=TextNode.ALeft,
                                    boxPlacement='left',
                                    state=DGG.DISABLED,
                                    command=self.handle_race_button,
                                    extraArgs=[race_index],
                                    text3_fg=(0.6, 0.6, 0.6, 1))
            btn.setOthers(self.race_buttons)
            self.race_buttons.append(btn)

    def display_alignment_picker(self):
        alignments = [alignment.Alignment.Lawful, alignment.Alignment.Neutral, alignment.Alignment.Chaotic]
        self.alignment_buttons = []
        for align_index, align_name in enumerate(alignments):
            self.alignments.append(align_name)
            btn = DirectRadioButton(parent=self.alignment_frame,
                                    text=str(align_name),
                                    scale=0.07,
                                    pos=(0.1, 0, -0.05 - (align_index * 0.1)),
                                    frameSize=(0, 10, -0.5, 1),
                                    text_pos=(1.2, 0),
                                    variable=self.selected_alignment,
                                    value=[align_name],
                                    others=self.alignment_buttons,
                                    text_font=self.label_font,
                                    text_align=TextNode.ALeft,
                                    boxPlacement='left',
                                    state=DGG.DISABLED,
                                    command=self.handle_alignment_button,
                                    extraArgs=[align_index],
                                    text3_fg=(0.6, 0.6, 0.6, 1))
            btn.setOthers(self.alignment_buttons)
            self.alignment_buttons.append(btn)