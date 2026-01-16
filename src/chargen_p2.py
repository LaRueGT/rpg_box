from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.gui.DirectCheckButton import DirectCheckButton

from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr

from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from DirectGuiExtension.DirectSpinBox import DirectSpinBox
from DirectGuiExtension.DirectGridSizer import DirectGridSizer

from panda3d.core import NodePath, TextNode

from direct.gui import DirectGuiGlobals as DGG

import alignment
import character
import diceroll
import pcclass
import race

class Chargen_p2(DirectObject):
    def __init__(self, base, ability_frame, button_frame, character_obj, modifiers_label, attacks_label, hp_label):
        super().__init__()
        self.base = base
        self.ability_frame = ability_frame
        self.button_frame = button_frame
        self.modifiers_label = modifiers_label
        self.attacks_label = attacks_label
        self.hp_label = hp_label
        self.label_font = self.base.loader.loadFont('../fonts/EBGaramond-VariableFont_wght.ttf')
        self.done_button = NodePath()
        self.new_char = character_obj
        self.base_stats = {
            "Strength": self.new_char.strength,
            "Intelligence": self.new_char.intelligence,
            "Wisdom": self.new_char.wisdom,
            "Dexterity": self.new_char.dexterity,
            "Constitution": self.new_char.constitution,
            "Charisma": self.new_char.charisma
        }
        self.stat_value_labels = {}
        self.stat_inc_buttons = {}
        self.stat_dec_buttons = {}
        self.adjustments = {"Strength": 0, "Intelligence": 0, "Wisdom": 0, "Dexterity": 0, "Constitution": 0, "Charisma": 0}
        self.adjustment_points = 0
        self.points_label = NodePath()

    def handle_next_button(self):
        def handle_next_button(self):
            if self.done_button['text'] == "Next":
                print("Next button pressed - calculating stats")
                self.calculate_modifiers()
                self.display_attack_values()
                # Disable all adjustment buttons to "commit" the stats
                for stat in self.stat_inc_buttons:
                    self.stat_inc_buttons[stat]['state'] = DGG.DISABLED
                    self.stat_dec_buttons[stat]['state'] = DGG.DISABLED
                if hasattr(self, 'reset_button'):
                    self.reset_button['state'] = DGG.DISABLED
                # Change button to Roll HP mode
                self.done_button['text'] = "Roll HP"
                self.done_button['state'] = DGG.NORMAL
            else:
                print("Rolling HP...")
                self.new_char.roll_hp()
                if self.hp_label:
                    self.hp_label['text'] = f"HP: {self.new_char.max_hp}"
                self.done_button['state'] = DGG.DISABLED

    def handle_reset_button(self):
        # Reset points and adjustment dictionary
        self.adjustment_points = 0
        for stat in self.adjustments:
            self.adjustments[stat] = 0
        # Manually update labels to base values immediately
        for stat, label in self.stat_value_labels.items():
            label['text'] = str(self.base_stats[stat])
        self.refresh_ui()

    def handle_cancel_button(self):
        print("cancel button pressed")
        messenger.send("chargen_cancel")

    def calculate_modifiers(self):
        # Update character object with final adjusted stats
        self.new_char.strength = self.base_stats["Strength"] + self.adjustments["Strength"]
        self.new_char.intelligence = self.base_stats["Intelligence"] + self.adjustments["Intelligence"]
        self.new_char.wisdom = self.base_stats["Wisdom"] + self.adjustments["Wisdom"]
        self.new_char.dexterity = self.base_stats["Dexterity"] + self.adjustments["Dexterity"]
        self.new_char.constitution = self.base_stats["Constitution"] + self.adjustments["Constitution"]
        self.new_char.charisma = self.base_stats["Charisma"] + self.adjustments["Charisma"]
        stats = [
            ("Strength", self.new_char.strength),
            ("Intelligence", self.new_char.intelligence),
            ("Wisdom", self.new_char.wisdom),
            ("Dexterity", self.new_char.dexterity),
            ("Constitution", self.new_char.constitution),
            ("Charisma", self.new_char.charisma),
        ]
        lines = ["Ability Score Modifiers"]
        for name, value in stats:
            mod = self.new_char.ability_modifier(value)
            sign = "+" if mod > 0 else ""
            lines.append(f"{name}: {sign}{mod}")
        if self.modifiers_label:
            self.modifiers_label['text'] = "\n".join(lines)

    def display_attack_values(self):
        thaco = 19
        attacks = self.new_char.get_attack_values(thaco)
        # Sort keys to ensure they line up correctly
        sorted_keys = sorted(attacks.keys())
        # Format rows
        row1 = "Attack Values (Target AC: Roll Needed)"
        header_parts = ["AC:  "]
        for k in sorted_keys:
            header_parts.append(f"{k:4}")
        row2 = "".join(header_parts)
        # Value row for Rolls: right-aligned in 4 spaces
        value_parts = ["Roll:"]
        for k in sorted_keys:
            value_parts.append(f"{attacks[k]:4}")
        row3 = "".join(value_parts)
        full_text = f"{row1}\n{row2}\n{row3}"
        if self.attacks_label:
            self.attacks_label['text'] = full_text

    def display_adjustment_boxes(self):
        z_offset = -0.15
        DirectLabel(
            parent=self.ability_frame,
            text="Adjust Ability Scores",
            text_font=self.label_font,
            text_scale=0.07,
            text_align=TextNode.ALeft,
            pos=(0.0, 0, 0),
            frameColor=(0, 0, 0, 0)
        )
        self.points_label = DirectLabel(
            parent=self.ability_frame,
            text=f"Points Available: {self.adjustment_points}",
            text_font=self.label_font,
            text_scale=0.05,
            text_align=TextNode.ALeft,
            pos=(0.0, 0, -0.08),
            frameColor=(0, 0, 0, 0)
        )
        for i, stat in enumerate(self.base_stats.keys()):
            z_pos = z_offset - (i * 0.12)
            DirectLabel(
                parent=self.ability_frame,
                text=stat,
                text_font=self.label_font,
                text_scale=0.06,
                text_align=TextNode.ALeft,
                pos=(0.0, 0, z_pos),
                frameColor=(0, 0, 0, 0)
            )
            self.stat_dec_buttons[stat] = DirectButton(
                parent=self.ability_frame,
                text="-",
                scale=0.07,
                frameSize=(-0.5, 0.5, -0.5, 0.5),
                pos=(0.40, 0, z_pos + 0.015),
                command=self.adjust_stat,
                extraArgs=[stat, -1],
                text3_fg=(0.6, 0.6, 0.6, 1)
            )
            self.stat_value_labels[stat] = DirectLabel(
                parent=self.ability_frame,
                text=str(self.base_stats[stat]),
                text_font=self.label_font,
                text_scale=0.06,
                pos=(0.50, 0, z_pos),
                frameColor=(0, 0, 0, 0)
            )
            self.stat_inc_buttons[stat] = DirectButton(
                parent=self.ability_frame,
                text="+",
                scale=0.07,
                frameSize=(-0.5, 0.5, -0.5, 0.5),
                pos=(0.60, 0, z_pos + 0.015),
                command=self.adjust_stat,
                extraArgs=[stat, 1],
                text3_fg=(0.6, 0.6, 0.6, 1)
            )
        self.refresh_ui()

    def adjust_stat(self, stat_name, delta):
        print(f"Adjusting {stat_name} by {delta}")
        current_val = self.base_stats[stat_name] + self.adjustments[stat_name]
        if delta > 0:  # Increase stat
            if self.adjustment_points <= 0 or current_val >= 18:
                return
            # undoing a previous reduction costs 1 point to gain 2 stat points back
            if self.adjustments[stat_name] < 0:
                self.adjustments[stat_name] += 2
            else:
                self.adjustments[stat_name] += 1
            self.adjustment_points -= 1
        elif delta < 0:  # Decrease stat
            if current_val -2 < 9:
                return
            # Lowering the stat by 2 gives the player 1 adjustment point
            self.adjustments[stat_name] -= 2
            self.adjustment_points += 1
        # Immediate value update for the label
        new_val = self.base_stats[stat_name] + self.adjustments[stat_name]
        self.stat_value_labels[stat_name]['text'] = str(new_val)
        # Debounce the state-wide UI refresh
        taskMgr.remove("refresh_ui_task")
        taskMgr.doMethodLater(0.05, self._deferred_refresh, "refresh_ui_task")

    def _deferred_refresh(self, task):
        self.refresh_ui()
        return task.done

    def refresh_ui(self):
        if self.points_label:
            self.points_label['text'] = f"Points Available: {self.adjustment_points}"
            # Only enable the Next button if all points are spent
            if self.done_button:
                if self.adjustment_points == 0:
                    self.done_button['state'] = DGG.NORMAL
                else:
                    self.done_button['state'] = DGG.DISABLED
        for stat in self.base_stats.keys():
            current_val = self.base_stats[stat] + self.adjustments[stat]
            inc_btn = self.stat_inc_buttons[stat]
            dec_btn = self.stat_dec_buttons[stat]
            # Default state
            inc_btn['state'] = DGG.NORMAL
            dec_btn['state'] = DGG.NORMAL
            # 1. Point Availability
            if self.adjustment_points <= 0:
                inc_btn['state'] = DGG.DISABLED
            # 2. Hard Limits
            if current_val >= 18:
                inc_btn['state'] = DGG.DISABLED
            if current_val - 2 < 9:
                dec_btn['state'] = DGG.DISABLED
            # 3. Class-based Restrictions
            stat_lower = stat.lower()
            if not pcclass.can_reduce(self.new_char.char_classes, stat_lower):
                dec_btn['state'] = DGG.DISABLED
            if stat_lower in ["dexterity", "constitution", "charisma"]:
                dec_btn['state'] = DGG.DISABLED
            is_prime = any(pcclass.is_prime_requisite(c, stat_lower) for c in self.new_char.char_classes)
            if not is_prime and self.adjustments[stat] >= 0:
                inc_btn['state'] = DGG.DISABLED

    def display_chargen_buttons(self):
        self.done_button = DirectButton(
            parent=self.button_frame,
            text="Next",
            scale=0.07,
            command=self.handle_next_button,
            text_font=self.label_font,
            text_align=TextNode.ALeft,
            text3_fg = (0.6, 0.6, 0.6, 1)
        )
        reset_button = DirectButton(
            parent=self.button_frame,
            text="Reset",
            scale=0.07,
            command=self.handle_reset_button,
            text_font=self.label_font,
            text_align=TextNode.ALeft,
            text3_fg=(0.6, 0.6, 0.6, 1)
        )
        cancel_button = DirectButton(
            parent=self.button_frame,
            text="Cancel",
            scale=0.07,
            command=self.handle_cancel_button,
            text_font=self.label_font,
            text_align=TextNode.ALeft,
            text3_fg=(0.6, 0.6, 0.6, 1)
        )
        self.button_frame.addItem(self.done_button)
        self.button_frame.addItem(reset_button)
        self.button_frame.addItem(cancel_button)
        # Initial UI refresh to set the Next button state
        self.refresh_ui()
