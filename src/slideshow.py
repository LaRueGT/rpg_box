from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CardMaker, NodePath

class slideshow(DirectObject.DirectObject):
    def __init__(self, base):
        super().__init__()
        self.ignore('escape')
        self.ignore('space')
        self.sequence = []
        self.position = 0
        self.active_slide = -1
        self.base_window = base
        self.base_frame = NodePath()
        self.art_frame = NodePath()
        self.text_frame = NodePath()
        self.card = NodePath()
        self.interrupt_flag = False
        self.accept('escape', self.interrupt_slide)
        self.accept('space', self.interrupt_slide)

    def centerfold_frame(self):
        self.base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                                 frameSize=(-1.778, 1.778, -1, 1),
                                 pos=(0, 0, 0))
        self.art_frame = DirectFrame(parent=self.base_frame,
                                frameColor=(0, 0, 0, 1),
                                frameSize=(-1.715, 1.715, -.88, .94),
                                pos=(0, 0, 0))

    def interrupt_slide(self):
        self.interrupt_flag = True

    def display_intro_sequence(self):
        self.sequence = ['../assets/slide1.png', '../assets/slide2.png', '../assets/slide3.png', '../assets/slide4.png', '../assets/slide5.png']
        self.centerfold_frame()
        cm = CardMaker("card")
        cm.setFrame(-1.715, 1.715, -.88, .94)
        self.card = self.art_frame.attachNewNode(cm.generate())
        taskMgr.add(self.display_slides, "display_slides")

    def display_slides(self, task):
        if self.active_slide != self.position:
            slide_tex = self.base_window.loader.loadTexture(self.sequence[self.position])
            self.card.setTexture(slide_tex)
            self.active_slide = self.position
        if task.time < 5.0 and self.interrupt_flag == False:
            return Task.cont
        else:
            self.interrupt_flag = False
            if self.position < len(self.sequence)-1:
                self.position += 1
                return Task.again
            else:
                return Task.done