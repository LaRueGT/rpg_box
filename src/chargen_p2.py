from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger

from direct.gui.DirectGui import DirectLabel
from direct.gui.DirectGui import DirectButton
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.gui.DirectCheckButton import DirectCheckButton

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
        self.stat_spinboxes = {}
        self.adjustments = {"Strength": 0, "Intelligence": 0, "Wisdom": 0, "Dexterity": 0, "Constitution": 0, "Charisma": 0}
        self.adjustment_points = 0

    def handle_next_button(self):
        print("Next button pressed")
        messenger.send("chargen_continue")

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
        # Define which stats can be increased based on class Prime Requisites
        class_names = [str(c) for c in self.new_char.char_classes]
        # todo prime req logic
        for i, (stat, value) in enumerate(self.base_stats.items()):
            # Create a label for the stat name (e.g., "STR")
            DirectLabel(
                parent=self.ability_frame,
                text=stat,
                text_font=self.label_font,
                text_scale=0.06,
                text_align=TextNode.ALeft,
                pos=(0.0, 0, z_offset - (i * 0.12)),
                frameColor=(0, 0, 0, 0)
            )
            # Create the SpinBox using DirectGuiExtension
            stat_spin = DirectSpinBox(
                parent=self.ability_frame,
                pos=(0.45, 0, z_offset - (i * 0.12)),
                scale=0.05,
                value=value,
                minValue=9,
                maxValue=18,
                command=self.update_stat,
                extraArgs=[stat]
            )
            # Setting color for state 3 (Disabled)
            stat_spin.incButton['text3_fg'] = (0.6, 0.6, 0.6, 1)
            stat_spin.decButton['text3_fg'] = (0.6, 0.6, 0.6, 1)
            self.stat_spinboxes[stat] = stat_spin
            if stat.lower() in ["dexterity", "constitution", "charisma"]:
                stat_spin.decButton['state'] = DGG.DISABLED
            # Class-based restriction on adjustments (e.g Thieves can lower Strength)
            if not pcclass.can_reduce(self.new_char.char_classes, stat.lower()):
                stat_spin.decButton['state'] = DGG.DISABLED
            # Only allow increasing Prime Requisites
            is_prime = any(pcclass.is_prime_requisite(c, stat.lower()) for c in self.new_char.char_classes)
            if not is_prime:
                stat_spin.incButton['state'] = DGG.DISABLED

    def update_stat(self, stat_name):
        # This will be called whenever a spinbox changes
        # You'll likely want to add logic here to track 'adjustment_points'
        print(f"Updated {stat_name}")

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
