from direct.gui.DirectGui import *
from panda3d.core import NodePath

class gui():
    def __init__(self,base):
        self.base_window = base
        self.base_window.aspect2d.node().removeAllChildren()

    def clear_gui(self):
        self.base_window.aspect2d.removeAllChildren()

    def centerfold_frame(self) -> NodePath:
        self.base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                                      frameSize=(-1.778, 1.778, -1, 1),
                                      pos=(0, 0, 0))
        self.art_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(0, 0, 0, 1),
                                     frameSize=(-1.715, 1.715, -.88, .94),
                                     pos=(0, 0, 0))
        return self.art_frame
