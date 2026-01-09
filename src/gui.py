from yaml import Node
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DirectLabel
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from DirectGuiExtension.DirectGridSizer import DirectGridSizer
from panda3d.core import NodePath, TextNode


class Gui:
    def __init__(self, base):
        self.base_window = base
        self.base_frame = DirectFrame(frameColor=(1, 1, 1, 1),
                                      frameSize=(-1.778, 1.778, -1, 1),
                                      pos=(0, 0, 0),
                                      frameTexture='../assets/wood_table_tex.jpg')
        self.art_frame = NodePath()
        self.cover_label_frame = NodePath()
        self.cover_label = NodePath()
        self.button_frame = NodePath()
        self.text_frame = NodePath()
        self.text_label = NodePath()
        self.chargen_screen_frame = NodePath()
        self.abilities_label = NodePath()
        self.race_heading = NodePath()
        self.racelist_frame = NodePath()
        self.alignment_heading = NodePath()
        self.alignment_frame = NodePath()
        self.classlist_frame = NodePath()
        self.label_font = self.base_window.loader.loadFont('../fonts/EBGaramond-VariableFont_wght.ttf')

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

    def chargen_frame(self) -> tuple[NodePath, NodePath, NodePath, NodePath, NodePath]:
        self.chargen_screen_frame = DirectFrame(parent=self.base_frame,
                                             frameColor=(.9, .9, .9, 1),
                                             frameSize=(-1.715, 1.715, -.88, .94),
                                             pos=(0, 0, 0),
                                             frameTexture='../assets/gridpaper_tex.png')
        self.abilities_label = DirectLabel(parent=self.chargen_screen_frame,
                                           text_font=self.label_font,
                                           text="Roll Ability Scores\nStrength:\t\tROLL READY\nIntelligence:\t\tROLL READY\nWisdom:\t\tROLL READY\nDexterity:\t\tROLL READY\nConstitution:\tROLL READY\nCharisma:\t\tROLL READY",
                                           text_scale=(0.07, 0.07),
                                           text_align=TextNode.ALeft,
                                           text_pos=(-1.65, 0.85),
                                           frameColor=(0, 0, 0, 0))
        self.racelist_frame = DirectFrame(parent=self.chargen_screen_frame,
                                          frameColor=(.25, .25, .25, 1),
                                          frameSize=(0, 0.8, -0.8, .0),
                                          pos=(-1.65, 0, 0.15))
        self.race_heading = DirectLabel(parent=self.racelist_frame,
                                   text="Choose Race",
                                   text_font=self.label_font,
                                   text_scale=0.07,
                                   text_align=TextNode.ALeft,
                                   pos=(0, 0, 0.05),
                                   frameColor=(0, 0, 0, 0))
        self.alignment_frame = DirectFrame(parent=self.chargen_screen_frame,
                                           frameColor=(.25, .25, .25, 1),
                                           frameSize=(0, 0.8, -0.3, .0),
                                           pos=(-0.75, 0, 0.15))
        self.alignment_heading = DirectLabel(parent=self.alignment_frame,
                                             text="Choose Alignment",
                                             text_font=self.label_font,
                                             text_scale=0.07,
                                             text_align=TextNode.ALeft,
                                             pos=(0, 0, 0.05),
                                             frameColor=(0, 0, 0, 0))
        self.classlist_frame = DirectFrame(parent=self.chargen_screen_frame,
                                           frameColor=(.25, .25, .25, 1),
                                           frameSize=(0, 0.8, -1.4, .0),
                                           pos=(0.15, 0, 0.75))
        self.class_heading = DirectLabel(parent=self.classlist_frame,
                                         text="Choose Classes (Max 3)",
                                         text_font=self.label_font,
                                         text_scale=0.07,
                                         text_align=TextNode.ALeft,
                                         pos=(0, 0, 0.05),
                                         frameColor=(0, 0, 0, 0))
        self.button_frame = DirectBoxSizer(orientation=DGG.HORIZONTAL,
                                           parent=self.base_frame,
                                           frameColor=(0, 0, 0, 1),
                                           frameSize=(-.25, .25, -.25, .25),
                                           pos=(-1.715, 0, -0.91))
        return self.abilities_label, self.racelist_frame, self.alignment_frame, self.classlist_frame, self.button_frame

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
