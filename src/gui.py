from direct.gui.DirectGui import *
from panda3d.core import NodePath

class Gui():
    def __init__(self,base):
        self.base_window = base
        self.base_window.aspect2d.node().removeAllChildren()

    def clear_gui(self):
        self.base_window.aspect2d.node().removeAllChildren()

    def centerfold_frame(self) -> NodePath:
        self.base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                                      frameSize=(-1.778, 1.778, -1, 1),
                                      pos=(0, 0, 0))
        self.art_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(0, 0, 0, 1),
                                     frameSize=(-1.715, 1.715, -.88, .94),
                                     pos=(0, 0, 0))
        return self.art_frame

    def narrative_frame(self) -> (NodePath, NodePath):
        self.base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                                      frameSize=(-1.778, 1.778, -1, 1),
                                      pos=(0, 0, 0))
        self.art_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(0, 0, 0, 1),
                                     frameSize=(-1.715, 1.715, -.48, .94),
                                     pos=(0, 0, 0))
        self.text_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(0, 0, 0, 1),
                                     frameSize=(-1.715, 1.715, -.88, -.47),
                                     pos=(0, 0, 0))
        self.text_label = DirectLabel(parent=self.text_frame,
                                      text="Initial Text",
                                      pos=(0, 0, 0))
        return self.art_frame, self.text_label