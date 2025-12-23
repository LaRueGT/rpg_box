from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CardMaker
from panda3d.core import NodePath


class Narrative(DirectObject):
    def __init__(self, base, frame, label):
        #placeholders and defaults
        super().__init__()
        self.picture_sequence = []
        self.narrative_text = {}
        self.picture_position = 0
        self.narrative_position = 0
        self.active_picture = -1
        self.active_narrative = -1
        self.card = NodePath()
        self.page_flag = False
        #setup
        self.base_window = base
        self.art_frame = frame
        self.label = label
        self.accept('enter', self.page_turn)
        self.accept('space', self.page_turn)

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
        cm.setFrame(-1.715, 1.715, -.46, .94)
        self.card = self.art_frame.attachNewNode(cm.generate())
        # Load the initial texture
        # initial_tex = self.base_window.loader.loadTexture(self.picture_sequence[0])
        # if initial_tex:
        #    self.card.setTexture(initial_tex)
        #    print("Initial texture loaded successfully")
        # else:
        #    print("Failed to load initial texture")
        # the image test should have loaded by now, wtf
        taskMgr.add(self.display_narrative, "display_narrative")

    def display_narrative(self, task):
        if self.active_picture != self.picture_position:
            picture_tex = self.base_window.loader.loadTexture(self.picture_sequence[self.picture_position])
            self.card.setTexture(picture_tex)
            self.active_picture = self.picture_position
            self.active_narrative = -1
            self.narrative_position = 0
            print(f"turning to picture {self.picture_position}, page is {self.narrative_position}")
        if self.active_narrative != self.narrative_position:
            self.label.setText(self.narrative_text[self.picture_position][self.narrative_position])
            self.active_narrative = self.narrative_position
            print(f"picture is {self.picture_position}, turning to page {self.narrative_position}")
        if not self.page_flag:
            return Task.cont
        else:
            self.page_flag = False
            if self.narrative_position < len(self.narrative_text[self.picture_position]) - 1:
                self.narrative_position += 1
                return Task.again
            if self.picture_position < len(self.picture_sequence) - 1:
                self.picture_position += 1
                return Task.again
            else:
                messenger.send("demo_finished")
                return Task.done