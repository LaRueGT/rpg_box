from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, NodePath

class slideshow(DirectObject.DirectObject):
    def __init__(self, base):
        self.ignore('escape')
        self.ignore('space')
        self.sequence = []
        self.position = 0
        self.base_window = base
        self.base_frame = NodePath()
        self.art_frame = NodePath()
        self.text_frame = NodePath()

    def centerfold_frame(self):
        self.base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                                 frameSize=(-1.778, 1.778, -1, 1),
                                 pos=(0, 0, 0))
        self.art_frame = DirectFrame(parent=self.base_frame,
                                frameColor=(0, 0, 0, 1),
                                frameSize=(-1.715, 1.715, -.88, .94),
                                pos=(0, 0, 0))

    def display_intro_sequence(self):
        self.sequence = ['../assets/slide1.png', '../assets/slide2.png', '../assets/slide3.png', '../assets/slide4.png', '../assets/slide5.png']
        self.centerfold_frame()
        cm = CardMaker("card")
        cm.setFrame(-1.715, 1.715, -.88, .94)
        card = self.art_frame.attachNewNode(cm.generate())
        slide = self.base_window.loader.loadTexture(self.sequence[self.position])
        card.setTexture(slide)
