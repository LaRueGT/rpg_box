from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectLabel
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from panda3d.core import NodePath


class Gui:
    def __init__(self,base):
        self.base_window = base
        self.base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                                      frameSize=(-1.778, 1.778, -1, 1),
                                      pos=(0, 0, 0))
        self.art_frame = NodePath()
        self.cover_label_frame = NodePath()
        self.cover_label = NodePath()
        self.button_frame = NodePath()
        self.text_frame = NodePath()
        self.text_label = NodePath()

    def clear_gui(self):
        self.base_frame.node().removeAllChildren()

    def centerfold_frame(self) -> NodePath:
        self.art_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(0, 0, 0, 1),
                                     frameSize=(-1.715, 1.715, -.88, .94),
                                     pos=(0, 0, 0))
        return self.art_frame

    def cover_frame(self) -> tuple[NodePath, NodePath]:
        self.cover_label_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(.25, .25, .25, 1),
                                     frameSize=(-1.715, 1.715, -.88, .94),
                                     pos=(0, 0, 0))
        self.cover_label = DirectLabel(parent=self.cover_label_frame,
                                      text="Initial Text",
                                      text_scale=(0.1, 0.1),
                                      pos=(0, 0, 0))
        self.button_frame = DirectBoxSizer(orientation=DGG.HORIZONTAL,
                                       parent=self.base_frame,
                                       frameColor=(0, 0, 0, 1),
                                       frameSize=(-.25, .25, -.25, .25),
                                       pos=(-1.715, 0, -0.91))
        return self.cover_label, self.button_frame

    def narrative_frame(self) -> tuple[NodePath, NodePath]:
        self.art_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(0, 0, 1, 1),
                                     frameSize=(-1.715, 1.715, -.46, .94),
                                     pos=(0, 0, 0))
        self.text_frame = DirectFrame(parent=self.base_frame,
                                     frameColor=(0, 1, 0, 1),
                                     frameSize=(-1.715, 1.715, -.205, 0.205),
                                     pos=(0, 0, -0.675))
        self.text_label = DirectLabel(parent=self.text_frame,
                                      text="Initial Text",
                                      text_scale=(0.1,0.1),
                                      text_pos=(0,-0.025))
        return self.art_frame, self.text_label