from yaml import Node
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectLabel
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from DirectGuiExtension.DirectGridSizer import DirectGridSizer
from DirectGuiExtension.DirectSpinBox import DirectSpinBox
from panda3d.core import NodePath, TextNode
from panda3d.core import TextProperties, TextPropertiesManager
from panda3d.core import TextureStage


class Gui:
    def __init__(self, base):
        self.base_window = base

        self.label_font = self.base_window.loader.loadFont('../fonts/EBGaramond-VariableFont_wght.ttf')
        tpm = TextPropertiesManager.getGlobalPtr()
        tp_red = TextProperties()
        tp_red.setTextColor(1.0, 0.0, 0.0, 1.0)  # Red (R, G, B, A)
        tpm.setProperties("red", tp_red)
        tp_green = TextProperties()
        tp_green.setTextColor(0.0, 1.0, 0.0, 1.0)  # Green
        tpm.setProperties("green", tp_green)
        tp_blue = TextProperties()
        tp_blue.setTextColor(0.0, 0.0, 1.0, 1.0)  # Blue
        tpm.setProperties("blue", tp_blue)
        self.base_frame = DirectFrame(frameColor=(1, 1, 1, 1),
                                      frameSize=(-1.778, 1.778, -1, 1),
                                      pos=(0, 0, 0),
                                      frameTexture='../assets/wood_table_tex.jpg')
        self.base_frame.guiItem.get_state_def(0).set_tex_scale(TextureStage.getDefault(), 1, 0.562)
        self.art_frame = NodePath()
        self.cover_label_frame = NodePath()
        self.cover_label = NodePath()
        self.button_frame = NodePath()
        self.text_frame = NodePath()
        self.text_label = NodePath()
        self.chargen_screen_frame = NodePath()

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

    def chargen_frame(self) -> tuple[NodePath, NodePath]:
        """Return the shared paper frame used by both chargen stages.

        Controls and labels belong to the chargen page.  Keeping only this
        common frame here lets the page own its widgets and presentation.
        """
        self.chargen_screen_frame = DirectFrame(parent=self.base_frame,
                                             frameColor=(1, 1, 1, 1),
                                             frameSize=(-1.715, 1.715, -.88, .94),
                                             pos=(0, 0, 0),
                                             frameTexture='../assets/gridpaper_tex.png')
        self.chargen_screen_frame.guiItem.get_state_def(0).set_tex_scale(TextureStage.getDefault(), 1, 0.53)
        self.chargen_button_frame = DirectBoxSizer(
            orientation=DGG.HORIZONTAL,
            parent=self.base_frame,
            frameColor=(0, 0, 0, 0),
            frameSize=(-.25, .25, -.25, .25),
            pos=(-1.715, 0, -.91),
        )
        return self.chargen_screen_frame, self.chargen_button_frame

    def main_frame(self) -> tuple[NodePath, NodePath]:
        self.text_frame = DirectFrame(parent=self.base_frame,
                                      frameColor=(0, 1, 1, 1),
                                      frameSize=(-1.715, 1.715, -.46, .94),
                                      pos=(0, 0, 0))
        self.text_label = DirectLabel(parent=self.text_frame,
                                      text_font=self.label_font,
                                      text="Initial Text",
                                      text_scale=(0.1, 0.1),
                                      text_pos=(0, -0.025),
                                      frameColor=(0, 0, 0, 0))
        self.button_frame = DirectGridSizer(numColumns=2, numRows=5,
                                            itemMargin=[0.01, 0.01, 0.01, 0.01],
                                            parent=self.base_frame,
                                            frameColor=(0, 1, 0, 1),
                                            frameSize=(-1.715, 1.715, -.205, 0.205),
                                            pos=(0, 0, -0.675))

        return self.text_label, self.button_frame

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
                                      text_font=self.label_font,
                                      text="Initial Text",
                                      text_scale=(0.07, 0.07),
                                      text_align=TextNode.ALeft,
                                      text_wordwrap=48,
                                      text_pos=(-1.65, 0.13),
                                      frameColor=(0, 0, 0, 0))
        return self.art_frame, self.text_label

    def party_assign_frame(self) -> tuple[NodePath, NodePath, NodePath]:
        self.cover_label_frame = DirectFrame(parent=self.base_frame,
                                             frameColor=(.25, .25, .25, 1),
                                             frameSize=(-1.715, 1.715, -.88, .94),
                                             pos=(0, 0, 0))
        self.cover_label = DirectLabel(parent=self.cover_label_frame,
                                       text="Select up to 6 Characters",
                                       text_scale=(0.1, 0.1),
                                       pos=(0, 0, 0.8))
        self.text_frame = DirectGridSizer(numColumns=3, numRows=10,
                                          parent=self.cover_label_frame,
                                          frameColor=(0, 0, 0, 0),
                                          pos=(0, 0, 0.6))
        self.button_frame = DirectBoxSizer(orientation=DGG.HORIZONTAL,
                                           parent=self.base_frame,
                                           frameColor=(0, 0, 0, 1),
                                           frameSize=(-.25, .25, -.25, .25),
                                           pos=(-1.715, 0, -0.91))
        return self.cover_label, self.text_frame, self.button_frame
