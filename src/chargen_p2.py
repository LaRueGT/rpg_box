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
    def __init__(self, base, ability_frame, button_frame, character_obj):
        super().__init__()
        self.base = base
        self.ability_frame = ability_frame
        self.button_frame = button_frame
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
        print("Next button pressed")
        messenger.send("chargenp2_finished")

    def handle_cancel_button(self):
        print("cancel button pressed")
        messenger.send("chargen_cancel")

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
        # Only allow change if logic permits (defensive check)
        if delta > 0 and self.adjustment_points <= 0:
            return
        self.adjustments[stat_name] += delta
        self.adjustment_points -= delta
        # Immediate value update for the label
        new_val = self.base_stats[stat_name] + self.adjustments[stat_name]
        self.stat_value_labels[stat_name]['text'] = str(new_val)
        # Debounce the state-wide UI refresh
        taskMgr.remove("refresh_ui_task")
        taskMgr.doMethodLater(0.01, self._deferred_refresh, "refresh_ui_task")

    def _deferred_refresh(self, task):
        self.refresh_ui()
        return task.done

    def refresh_ui(self):
        if self.points_label:
            self.points_label['text'] = f"Points Available: {self.adjustment_points}"

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
            if current_val <= 9:
                dec_btn['state'] = DGG.DISABLED
            # 3. Class-based Restrictions
            stat_lower = stat.lower()
            if not pcclass.can_reduce(self.new_char.char_classes, stat_lower):
                dec_btn['state'] = DGG.DISABLED
            if stat_lower in ["dexterity", "constitution", "charisma"]:
                dec_btn['state'] = DGG.DISABLED
            is_prime = any(pcclass.is_prime_requisite(c, stat_lower) for c in self.new_char.char_classes)
            if not is_prime:
                inc_btn['state'] = DGG.DISABLED

    def display_chargen_buttons(self):
        self.done_button = DirectButton(
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
        self.button_frame.addItem(self.done_button)
        self.button_frame.addItem(cancel_button)
