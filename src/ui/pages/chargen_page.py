from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectGui import DGG, DirectButton, DirectEntry, DirectLabel
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from panda3d.core import NodePath, TextNode

from model import alignment
from model import pcclass
from model import race
from model.character import Character
from rules import character_creation
from rules import combat_rules, leveling_rules
from direct.task.TaskManagerGlobal import taskMgr

class Chargen(DirectObject):
    """Character creation flow and its page-specific widgets.
    gui.py supplies only the shared paper frame;
    this class owns the controls and translates user
    actions into the chargen events consumed by masterFSM.
    """

    def __init__(self, base, ui, character_obj=None):
        super().__init__()
        self.base = base
        self.ui = ui
        self.screen_frame = ui.make_grid_paper_page()
        self.button_frame = ui.make_button_row(frame_color=(0, 0, 0, 0))
        self.roll_button = NodePath()
        self.label_font = ui.label_font
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
        self.new_char = character_obj or Character()
        self.base_stats = {
            ability_name: 0
            for ability_name in character_creation.ABILITY_NAMES
        }

    def display_first_page(self):
        """Build the race, alignment, gender, and class selection page."""
        self.ability_label = DirectLabel(parent=self.screen_frame, text_font=self.label_font,
                                         text_scale=(0.07, 0.07),
                                         text="Roll Ability Scores\n" + "\n".join(
                                             f"{name.title()}: ROLL READY"
                                             for name in character_creation.ABILITY_NAMES),
                                         text_align=TextNode.ALeft, text_pos=(-1.665, 0.85),
                                         frameColor=(0, 0, 0, 0))
        self.race_list_frame = self._picker_frame((-1.665, 0, 0.15), 0.8, -0.8)
        self.alignment_frame = self._picker_frame((-0.969, 0, 0.15), 0.8, -0.3)
        self.gender_frame = self._picker_frame((-0.969, 0, -0.35), 0.8, -0.2)
        self.class_list_frame = self._picker_frame((-.19, 0, 0.8), 0.8, -1.4)
        for frame, title in ((self.race_list_frame, "Choose Race"),
                             (self.alignment_frame, "Choose Alignment"),
                             (self.gender_frame, "Choose Gender"),
                             (self.class_list_frame, "Choose Classes (Max 3)")):
            DirectLabel(parent=frame, text=title, text_font=self.label_font, text_scale=0.07,
                        text_align=TextNode.ALeft, pos=(0, 0, 0.05), frameColor=(0, 0, 0, 0))
        self.button_frame = self._button_frame()
        self.display_chargen_buttons()
        self.display_race_picker()
        self.display_alignment_picker()
        self.display_gender_picker()
        self.display_class_picker()

    def display_second_page(self):
        """Replace the first page with the ability adjustment page."""
        self.screen_frame.node().removeAllChildren()
        self.ability_frame = self._picker_frame((-1.665, 0, 0.85), 0.8, -0.6)
        self.modifiers_label = DirectLabel(parent=self.screen_frame, text_font=self.label_font,
                                           text_scale=0.07, text="Ability Score Modifiers",
                                           text_align=TextNode.ALeft, pos=(-0.8, 0, 0.85),
                                           frameColor=(0, 0, 0, 0))
        self.attacks_label = DirectLabel(parent=self.screen_frame, text_font=self.label_font,
                                         text_scale=0.07, text="Attack Values",
                                         text_align=TextNode.ALeft, pos=(-0.8, 0, 0.15),
                                         frameColor=(0, 0, 0, 0))
        self.hp_label = DirectLabel(parent=self.screen_frame, text_font=self.label_font,
                                    text_scale=0.07, text="HP: ROLL READY",
                                    text_align=TextNode.ALeft, pos=(-0.8, 0, -0.15),
                                    frameColor=(0, 0, 0, 0))
        self.button_frame = self._button_frame()
        self.base_stats = character_creation.get_base_stats(self.new_char)
        self.stat_value_labels = {}
        self.stat_inc_buttons = {}
        self.stat_dec_buttons = {}
        self.adjustments = {name: 0 for name in character_creation.ABILITY_NAMES}
        self.adjustment_points = 0
        self.points_label = NodePath()
        self.display_adjustment_boxes()
        self.display_second_page_buttons()

    def _picker_frame(self, pos, right, bottom):
        from direct.gui.DirectGui import DirectFrame
        return DirectFrame(parent=self.screen_frame, frameColor=(.25, .25, .25, 0),
                           frameSize=(0, right, bottom, .0), pos=pos)

    def _button_frame(self):
        return self.button_frame or DirectBoxSizer(
            orientation=DGG.HORIZONTAL, parent=self.screen_frame,
            frameColor=(0, 0, 0, 0), frameSize=(-.25, .25, -.25, .25),
            pos=(-1.715, 0, -.91))

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
        # Character levels are stored per class.  A new character starts at
        # level 1 in every selected class, rather than only in the default
        # single-class slot created by Character.
        self.new_char.level = [1] * len(self.selected_classes)
        leveling_rules.update_saving_throws(self.new_char)
        # Update experience factors for all selected classes
        self.new_char.exp_factor = character_creation.calculate_exp_factors(
            self.new_char,
            self.selected_classes,
        )
        print(f"XP Factors: {[str(c) for c in self.new_char.exp_factor]}")
        self.update_class_buttons()

    def handle_first_page_next(self):
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
            command=self.handle_first_page_next,
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

    # --- second chargen stage -------------------------------------------------
    def display_adjustment_boxes(self):
        DirectLabel(parent=self.ability_frame, text="Adjust Ability Scores",
                    text_font=self.label_font, text_scale=0.07, text_align=TextNode.ALeft,
                    pos=(0, 0, 0), frameColor=(0, 0, 0, 0))
        self.points_label = DirectLabel(parent=self.ability_frame,
                                        text="Points Available: 0", text_font=self.label_font,
                                        text_scale=0.05, text_align=TextNode.ALeft,
                                        pos=(0, 0, -0.08), frameColor=(0, 0, 0, 0))
        for index, stat in enumerate(self.base_stats):
            z_pos = -0.15 - index * 0.12
            DirectLabel(parent=self.ability_frame, text=stat, text_font=self.label_font,
                        text_scale=0.06, text_align=TextNode.ALeft, pos=(0, 0, z_pos),
                        frameColor=(0, 0, 0, 0))
            self.stat_dec_buttons[stat] = DirectButton(parent=self.ability_frame, text="-",
                scale=.07, pos=(.40, 0, z_pos + .015), command=self.adjust_stat,
                extraArgs=[stat, -1], text3_fg=(.6, .6, .6, 1))
            self.stat_value_labels[stat] = DirectLabel(parent=self.ability_frame,
                text=str(self.base_stats[stat]), text_font=self.label_font, text_scale=.06,
                pos=(.50, 0, z_pos), frameColor=(0, 0, 0, 0))
            self.stat_inc_buttons[stat] = DirectButton(parent=self.ability_frame, text="+",
                scale=.07, pos=(.60, 0, z_pos + .015), command=self.adjust_stat,
                extraArgs=[stat, 1], text3_fg=(.6, .6, .6, 1))
        self.refresh_ui()

    def adjust_stat(self, stat_name, delta):
        current = self.base_stats[stat_name] + self.adjustments[stat_name]
        if delta > 0:
            if self.adjustment_points <= 0 or current >= 18:
                return
            self.adjustments[stat_name] += 2 if self.adjustments[stat_name] < 0 else 1
            self.adjustment_points -= 1
        elif current - 2 >= 9 and pcclass.can_reduce(self.new_char.char_classes, stat_name.lower()):
            if stat_name.lower() not in {"dexterity", "constitution", "charisma"}:
                self.adjustments[stat_name] -= 2
                self.adjustment_points += 1
        self.stat_value_labels[stat_name]['text'] = str(self.base_stats[stat_name] + self.adjustments[stat_name])
        taskMgr.remove("refresh_chargen_ui")
        taskMgr.doMethodLater(.05, self._deferred_refresh, "refresh_chargen_ui")

    def _deferred_refresh(self, task):
        self.refresh_ui()
        return task.done

    def refresh_ui(self):
        self.points_label['text'] = f"Points Available: {self.adjustment_points}"
        for stat in self.base_stats:
            value = self.base_stats[stat] + self.adjustments[stat]
            inc, dec = self.stat_inc_buttons[stat], self.stat_dec_buttons[stat]
            inc['state'] = DGG.NORMAL if self.adjustment_points and value < 18 else DGG.DISABLED
            can_reduce = (value - 2 >= 9 and stat.lower() not in {"dexterity", "constitution", "charisma"}
                          and pcclass.can_reduce(self.new_char.char_classes, stat.lower()))
            dec['state'] = DGG.NORMAL if can_reduce else DGG.DISABLED
            if not any(pcclass.is_prime_requisite(c, stat.lower()) for c in self.new_char.char_classes):
                inc['state'] = DGG.DISABLED
        if getattr(self, 'done_button', None):
            self.done_button['state'] = DGG.NORMAL if self.adjustment_points == 0 else DGG.DISABLED

    def display_second_page_buttons(self):
        self.done_button = DirectButton(parent=self.button_frame, text="Next", scale=.07,
                                        command=self.handle_next_button, text_font=self.label_font,
                                        text_align=TextNode.ALeft, text3_fg=(.6, .6, .6, 1))
        self.reset_button = DirectButton(parent=self.button_frame, text="Reset", scale=.07,
                                         command=self.handle_reset_button, text_font=self.label_font)
        cancel_button = DirectButton(parent=self.button_frame, text="Cancel", scale=.07,
                                     command=self.handle_cancel_button, text_font=self.label_font)
        for button in (self.done_button, self.reset_button, cancel_button):
            self.button_frame.addItem(button)
        self.refresh_ui()

    def handle_reset_button(self):
        self.adjustment_points = 0
        self.adjustments = {name: 0 for name in self.adjustments}
        for stat, label in self.stat_value_labels.items():
            label['text'] = str(self.base_stats[stat])
        self.refresh_ui()

    def handle_next_button(self):
        current = self.done_button['text']
        current = current[0] if isinstance(current, tuple) else current
        if current == "Next":
            self.calculate_modifiers()
            self.display_attack_values()
            for button in (*self.stat_inc_buttons.values(), *self.stat_dec_buttons.values()):
                button['state'] = DGG.DISABLED
            self.reset_button['state'] = DGG.DISABLED
            self.done_button['text'] = "Roll HP"
            self.done_button['state'] = DGG.NORMAL
        else:
            leveling_rules.roll_hp_for_character(self.new_char)
            self.hp_label['text'] = f"HP: {self.new_char.max_hp}"
            self.done_button['state'] = DGG.DISABLED
            self.reveal_name_entry()

    def calculate_modifiers(self):
        character_creation.apply_ability_adjustments(self.new_char, self.base_stats, self.adjustments)
        self.modifiers_label['text'] = "\n".join(character_creation.build_modifier_lines(self.new_char))

    def display_attack_values(self):
        attacks = combat_rules.get_attack_values(self.new_char.thaco)
        keys = sorted(attacks)
        self.attacks_label['text'] = ("Attack Values (Target AC: Roll Needed)\nAC:  "
            + ''.join(f"{key:4}" for key in keys) + "\nRoll:"
            + ''.join(f"{attacks[key]:4}" for key in keys))

    def reveal_name_entry(self):
        frame = DirectBoxSizer(orientation=DGG.HORIZONTAL, parent=self.screen_frame,
                               frameColor=(0, 0, 0, 0), pos=(-1.665, 0, -.75))
        DirectLabel(parent=frame, text="Character Name: ", text_font=self.label_font,
                    text_scale=.07, frameColor=(0, 0, 0, 0))
        self.name_entry = DirectEntry(parent=frame, text_font=self.label_font, scale=.07,
                                      width=15, numLines=1, focus=1, cursorKeys=1,
                                      command=self.handle_name_submit)
        submit = DirectButton(parent=frame, text="Submit", scale=.07,
                              text_font=self.label_font, command=self.handle_name_submit)
        for item in (self.name_entry, submit):
            frame.addItem(item)

    def handle_name_submit(self, submitted_text=None):
        name = submitted_text if submitted_text is not None else self.name_entry.get()
        if name and name.strip():
            self.new_char.name = name.strip()
            messenger.send("chargen_done", [self.new_char])
