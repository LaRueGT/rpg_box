from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CardMaker, NodePath

class Slideshow(DirectObject):
    def __init__(self, base, frame):
        #placeholders and defaults
        super().__init__()
        self.ignore('escape')
        self.ignore('space')
        self.sequence = []
        self.position = 0
        self.active_slide = -1
        self.card = NodePath()
        self.interrupt_flag = False
        #setup
        self.base_window = base
        self.art_frame = frame
        self.accept('escape', self.interrupt_slide)
        self.accept('space', self.interrupt_slide)

    def interrupt_slide(self):
        self.interrupt_flag = True

    def display_intro_sequence(self):
        self.sequence = ['../assets/slide1.png', '../assets/slide2.png', '../assets/slide3.png', '../assets/slide4.png', '../assets/slide5.png']
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
                messenger.send("slide_finished")
                return Task.done