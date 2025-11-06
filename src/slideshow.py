from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from panda3d.core import CardMaker

def display_intro_sequence(self):
    color_sequence = [(0, 0, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (0, 1, 0, 1)]
    sequence_position = 0
    # intro panel
    base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                             frameSize=(-1.778, 1.778, -1, 1),
                             pos=(0, 0, 0))
    art_frame = DirectFrame(parent=base_frame,
                            frameColor=(0, 0, 0, 1),
                            frameSize=(-1.715, 1.715, -.88, .94),
                            pos=(0, 0, 0))