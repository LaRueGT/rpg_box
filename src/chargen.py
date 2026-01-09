import alignment
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton, DGG
from panda3d.core import TextNode, NodePath
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.gui.DirectCheckButton import DirectCheckButton
from direct.showbase.MessengerGlobal import messenger

import diceroll
import character
import race
import pcclass

class Chargen(DirectObject):
    def __init__(self, base, ability_label, racelist_frame, alignment_frame, classlist_frame, button_frame):
        super().__init__()
        self.base = base
        self.ability_label = ability_label
        self.race_list_frame = racelist_frame
        self.alignment_frame = alignment_frame
        self.class_list_frame = classlist_frame
        self.button_frame = button_frame
        self.roll_button = NodePath()
        self.label_font = self.base.loader.loadFont('../fonts/EBGaramond-VariableFont_wght.ttf')
        self.races = []
        self.race_buttons = []
        self.selected_race = [None]
        self.alignments = []
        self.alignment_buttons = []
        self.selected_alignment = [None]
        self.class_buttons = []
        self.selected_classes = []
        self.new_char = character.Character()
        self.base_stats = {"str": 0, "int": 0, "wis": 0, "dex": 0, "con": 0, "cha": 0}

    def handle_roll_button(self):
        print("roll button pressed")
        self.roll_button['state'] = DGG.DISABLED
        self.base_stats["str"] = diceroll.roll(3, 6)
        self.base_stats["int"] = diceroll.roll(3, 6)
        self.base_stats["wis"] = diceroll.roll(3, 6)
        self.base_stats["dex"] = diceroll.roll(3, 6)
        self.base_stats["con"] = diceroll.roll(3, 6)
        self.base_stats["cha"] = diceroll.roll(3, 6)
        # Initialize char stats with base rolls
        self.new_char.strength = self.base_stats["str"]
        self.new_char.intelligence = self.base_stats["int"]
        self.new_char.wisdom = self.base_stats["wis"]
        self.new_char.dexterity = self.base_stats["dex"]
        self.new_char.constitution = self.base_stats["con"]
        self.new_char.charisma = self.base_stats["cha"]
        self.update_ability_label()
        for race_index in range(len(self.races)):
            if race.meets_requirements(self.races[race_index], self.new_char.strength, self.new_char.intelligence, self.new_char.wisdom, self.new_char.dexterity, self.new_char.constitution, self.new_char.charisma):
                self.race_buttons[race_index]['state'] = DGG.NORMAL
        for btn in self.alignment_buttons:
            btn['state'] = DGG.NORMAL

    def update_ability_label(self):
        stats = [
            ("Strength", self.new_char.strength, self.base_stats["str"]),
            ("Intelligence", self.new_char.intelligence, self.base_stats["int"]),
            ("Wisdom", self.new_char.wisdom, self.base_stats["wis"]),
            ("Dexterity", self.new_char.dexterity, self.base_stats["dex"]),
            ("Constitution", self.new_char.constitution, self.base_stats["con"]),
            ("Charisma", self.new_char.charisma, self.base_stats["cha"]),
        ]
        lines = ["Roll Ability Scores"]
        for name, current, base in stats:
            color_tag = ""
            if current > base:
                color_tag = "\1green\1"
            elif current < base:
                color_tag = "\1red\1"
            lines.append(f"{name}: {color_tag}{current}\2")
        self.ability_label['text'] = "\n".join(lines)

    def update_class_buttons(self):
        #Enables or disables class buttons based on requirements and the 3-selection limit
        if self.new_char.char_race is None or self.new_char.char_alignment is None:
            for btn in self.class_buttons:
                btn['state'] = DGG.DISABLED
            return
        num_selected = len(self.selected_classes)
        for btn in self.class_buttons:
            cls = btn['extraArgs'][0]
            meets = pcclass.meets_requirements(
                cls, self.new_char.char_race, self.new_char.char_alignment,
                self.new_char.strength, self.new_char.intelligence, self.new_char.wisdom,
                self.new_char.dexterity, self.new_char.constitution, self.new_char.charisma
            )
            if not meets:
                btn['state'] = DGG.DISABLED
            elif num_selected >= 3 and cls not in self.selected_classes:
                btn['state'] = DGG.DISABLED
            else:
                btn['state'] = DGG.NORMAL

    def handle_race_button(self, race_index):
        new_race = self.races[race_index]
        if self.new_char.char_race == new_race:
            return
        self.new_char.char_race = self.races[race_index]
        print(f"Selected race: {self.new_char.char_race.name}")
        # Apply modifiers from base stats
        mods = race.get_stat_mods(new_race)
        self.new_char.strength = self.base_stats["str"] + mods[0]
        self.new_char.intelligence = self.base_stats["int"] + mods[1]
        self.new_char.wisdom = self.base_stats["wis"] + mods[2]
        self.new_char.dexterity = self.base_stats["dex"] + mods[3]
        self.new_char.constitution = self.base_stats["con"] + mods[4]
        self.new_char.charisma = self.base_stats["cha"] + mods[5]
        self.update_ability_label()
        self.update_class_buttons()
        # Clear existing class selections
        self.selected_classes = []
        for btn in self.class_buttons:
            btn['indicatorValue'] = 0
            btn.setIndicatorValue()
        self.update_class_buttons()

    def handle_alignment_button(self, align_index):
        if self.new_char.char_alignment == self.alignments[align_index]:
            return
        self.new_char.char_alignment = self.alignments[align_index]
        print(f"Selected alignemnt: {self.new_char.char_alignment.name}")
        self.update_class_buttons()
        # Clear existing class selections
        self.selected_classes = []
        for btn in self.class_buttons:
            btn['indicatorValue'] = 0
            btn.setIndicatorValue()
        self.update_class_buttons()

    def handle_class_button(self, status, pc_class):
        if status:
            if pc_class not in self.selected_classes:
                self.selected_classes.append(pc_class)
        else:
            if pc_class in self.selected_classes:
                self.selected_classes.remove(pc_class)

        print(f"Selected classes: {[str(c) for c in self.selected_classes]}")
        self.update_class_buttons()

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
                                    frameSize=(0, 6, -0.5, 1),
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
                                    frameSize=(0, 5, -0.5, 1),
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

    def display_class_picker(self):
        self.class_buttons = []
        for class_index, class_option in enumerate(pcclass.PCClass):
            btn = DirectCheckButton(parent=self.class_list_frame,
                                    text=str(class_option),
                                    scale=0.07,
                                    pos=(0.1, 0, -0.05 - (class_index * 0.1)),
                                    frameSize=(0, 7, -0.5, 1),
                                    text_pos=(1.2, 0),
                                    text_font=self.label_font,
                                    text_align=TextNode.ALeft,
                                    boxPlacement='left',
                                    state=DGG.DISABLED,
                                    command=self.handle_class_button,
                                    extraArgs=[class_option],
                                    text3_fg=(0.6, 0.6, 0.6, 1))
            self.class_buttons.append(btn)