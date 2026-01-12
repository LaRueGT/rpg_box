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
    def __init__(self, base, ability_frame, button_frame):
        super().__init__()
        self.base = base
        self.ability_frame = ability_frame
        self.button_frame = button_frame
        self.label_font = self.base.loader.loadFont('../fonts/EBGaramond-VariableFont_wght.ttf')
        self.done_button = NodePath()
        self.new_char = character.Character()
        self.base_stats = {"str": 0, "int": 0, "wis": 0, "dex": 0, "con": 0, "cha": 0}
        self.adjustments = {"str": 0, "int": 0, "wis": 0, "dex": 0, "con": 0, "cha": 0}
        self.adjustment_points = 0

    def handle_next_button(self):
        print("Next button pressed")
        messenger.send("chargen_continue")

    def handle_cancel_button(self):
        print("cancel button pressed")
        messenger.send("chargen_cancel")

    def display_adjustment_boxes(self):
        z_offset = -0.15
        for i, (stat, value) in enumerate(self.base_stats.items()):
            # Create a label for the stat name (e.g., "STR")
            DirectLabel(
                parent=self.ability_frame,
                text=stat.upper(),
                text_font=self.label_font,
                text_scale=0.06,
                text_align=TextNode.ALeft,
                pos=(0.0, 0, z_offset - (i * 0.12)),
                frameColor=(0, 0, 0, 0)
            )
            # Create the SpinBox using DirectGuiExtension
            # Note: value is the starting point, items sets the range
            stat_spin = DirectSpinBox(
                parent=self.ability_frame,
                pos=(0.35, 0, z_offset - (i * 0.12)),
                scale=0.05,
                value=value,
                minValue=9,
                maxValue=18,
                command=self.update_stat,
                extraArgs=[stat]
            )

    def update_stat(self, stat_name):
        # This will be called whenever a spinbox changes
        # You'll likely want to add logic here to track 'adjustment_points'
        print(f"Updated {stat_name}")

    def display_chargen_buttons(self):
        self.done_button = DirectButton(
            parent=self.button_frame,
            text="Next",
            text_font=self.label_font,
            text_scale=0.1,
            command=self.handle_next_button,
            frameColor=(0, 0, 0, 0)
        )