from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectGui import DGG, DirectButton
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from panda3d.core import NodePath, TextNode

from model import alignment
from model import pcclass
from model import race
from model.character import Character
from rules import character_creation

class Chargen(DirectObject):
    def __init__(self, base, ability_label, racelist_frame, alignment_frame, gender_frame, classlist_frame, button_frame):
        super().__init__()
        self.base = base
        self.ability_label = ability_label
        self.race_list_frame = racelist_frame
        self.alignment_frame = alignment_frame
        self.gender_frame = gender_frame
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
        self.gender_buttons = []
        self.selected_gender = [None]
        self.class_buttons = []
        self.selected_classes = []
        self.new_char = Character()
        self.base_stats = {
            ability_name: 0
            for ability_name in character_creation.ABILITY_NAMES
        }

    def handle_roll_button(self):
        print("roll button pressed")
        self.roll_button['state'] = DGG.DISABLED
        self.base_stats = character_creation.roll_base_stats()
        character_creation.apply_base_stats(self.new_char, self.base_stats)
        self.update_ability_label()
        for race_index in range(len(self.races)):
            if race.meets_requirements(self.races[race_index], self.new_char.strength, self.new_char.intelligence, self.new_char.wisdom, self.new_char.dexterity, self.new_char.constitution, self.new_char.charisma):
                self.race_buttons[race_index]['state'] = DGG.NORMAL
        for btn in self.alignment_buttons:
            btn['state'] = DGG.NORMAL
        for btn in self.gender_buttons:
            btn['state'] = DGG.NORMAL

    def update_ability_label(self):
        lines = character_creation.build_ability_score_lines(
            self.new_char,
            self.base_stats,
        )
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
            # Calculate prime requisite factor and determine color
            factor = pcclass.prime_requisite_factor(
                cls, self.new_char.strength, self.new_char.dexterity, self.new_char.constitution,
                self.new_char.intelligence, self.new_char.wisdom, self.new_char.charisma
            )
            # color mapping: dark red, red, black, green, blue
            if factor <= 0.8:
                color = (0.5, 0, 0, 1)
            elif factor <= 0.9:
                color = (1, 0, 0, 1)
            elif factor >= 1.1:
                color = (0, 0, 1, 1)
            elif factor >= 1.05:
                color = (0, 0.5, 0, 1)
            else:
                color = (0, 0, 0, 1)
            btn['text_fg'] = color
            if not meets:
                btn['state'] = DGG.DISABLED
                btn['text_fg'] = (0.6, 0.6, 0.6, 1)  # Force gray if requirements not met
            elif num_selected >= 3 and cls not in self.selected_classes:
                btn['state'] = DGG.DISABLED
                btn['text_fg'] = (0.6, 0.6, 0.6, 1)  # Force gray if limit reached
            else:
                btn['state'] = DGG.NORMAL
                btn['text_fg'] = color

    def handle_race_button(self, race_index):
        new_race = self.races[race_index]
        if self.new_char.char_race == new_race:
            return
        self.new_char.char_race = self.races[race_index]
        print(f"Selected race: {self.new_char.char_race.name}")
        # Apply modifiers from base stats
        mods = race.get_stat_mods(new_race)
        character_creation.apply_race_modifiers(
            self.new_char,
            self.base_stats,
            mods,
        )
        self.update_ability_label()
        self.update_class_buttons()
        # Clear existing class selections
        self.selected_classes = []
        for btn in self.class_buttons:
            btn["indicatorValue"] = 0
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

    def handle_gender_button(self, gender):
        self.new_char.gender = gender
        print(f"Selected gender: {gender}")

    def handle_class_button(self, status, pc_class):
        if status:
            if pc_class not in self.selected_classes:
                self.selected_classes.append(pc_class)
        else:
            if pc_class in self.selected_classes:
                self.selected_classes.remove(pc_class)
        self.selected_classes.sort(key=lambda c: str(c))
        print(f"Selected classes: {[str(c) for c in self.selected_classes]}")
        self.new_char.char_classes = self.selected_classes
        # Update experience factors for all selected classes
        self.new_char.exp_factor = character_creation.calculate_exp_factors(
            self.new_char,
            self.selected_classes,
        )
        print(f"XP Factors: {[str(c) for c in self.new_char.exp_factor]}")
        self.update_class_buttons()

    def handle_next_button(self):
        print("Next button pressed")
        messenger.send("chargen_continue")

    def handle_cancel_button(self):
        print("cancel button pressed")
        messenger.send("chargen_cancel")

    def display_chargen_buttons(self):
        self.roll_button = DirectButton(
            parent=self.button_frame,
            text="Roll Stats",
            scale=.07,
            command=self.handle_roll_button,
            text_font=self.label_font,
            text_align=TextNode.ALeft,
            text_fg=(0, 0, 0, 1),
            text3_fg=(0.6, 0.6, 0.6, 1)  # Color for state 3 (Disabled)
        )
        next_button = DirectButton(
            parent=self.button_frame,
            text="Next",
            scale=0.07,
            command=self.handle_next_button,
            text_font=self.label_font,
            text_align=TextNode.ALeft
        )
        cancel_button = DirectButton(
            parent=self.button_frame,
            text="Cancel",
            scale=0.07,
            command=self.handle_cancel_button,
            text_font=self.label_font,
            text_align=TextNode.ALeft
        )
        self.button_frame.addItem(self.roll_button)
        self.button_frame.addItem(next_button)
        self.button_frame.addItem(cancel_button)

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

    def display_gender_picker(self):
        genders = ["Male", "Female"]
        self.gender_buttons = []
        for g_index, g_name in enumerate(genders):
            btn = DirectRadioButton(parent=self.gender_frame,
                                    text=g_name,
                                    scale=0.07,
                                    pos=(0.1, 0, -0.05 - (g_index * 0.1)),
                                    frameSize=(0, 5, -0.5, 1),
                                    text_pos=(1.2, 0),
                                    variable=self.selected_gender,
                                    value=[g_name],
                                    others=self.gender_buttons,
                                    text_font=self.label_font,
                                    text_align=TextNode.ALeft,
                                    boxPlacement='left',
                                    state=DGG.DISABLED,
                                    command=self.handle_gender_button,
                                    extraArgs=[g_name],
                                    text3_fg=(0.6, 0.6, 0.6, 1))
            btn.setOthers(self.gender_buttons)
            self.gender_buttons.append(btn)

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