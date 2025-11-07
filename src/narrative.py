from direct.showbase import DirectObject
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CardMaker, NodePath

class Narrative(DirectObject.DirectObject):
    def __init__(self, base, card, label):
        #placeholders and defaults
        super().__init__()
        self.ignore('enter')
        self.ignore('space')
        self.picture_sequence = []
        self.narrative_text = {}
        self.picture_position = 0
        self.narrative_position = 0
        self.active_picture = -1
        self.active_narrative = -1
        self.base_window = base
        self.picture_frame = NodePath()
        self.text_frame = NodePath()
        self.card = NodePath()
        self.label = NodePath()
        self.page_flag = False
        #setup
        self.accept('enter', self.page_turn)
        self.accept('space', self.page_turn )

        def page_turn(self):
            self.page_flag = True

        def display_dummy_narrative(self):
            self.picture_sequence = ['../assets/slide1.png', '../assets/slide2.png', '../assets/slide3.png',
                             '../assets/slide4.png', '../assets/slide5.png']
            self.narrative_text = {0: ['slide1 - page1', 'slide1 - page2'],
                                   1: ['slide2 - page1', 'slide2 - page2', 'slide2 - page3'],
                                   2: ['slide3 - page1'],
                                   3: ['slide4 - page1'],
                                   4: ['slide5 - page1', 'slide5 - page2', 'slide5 - page3', 'slide5 - page4', 'slide5 - page5']}
            cm = CardMaker("card")
            cm.setFrame(-1.715, 1.715, -.88, .94)
            self.card = self.picture_frame.attachNewNode(cm.generate())
            taskMgr.add(self.display_slides, "display_slides")