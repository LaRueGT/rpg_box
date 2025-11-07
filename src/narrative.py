from direct.showbase import DirectObject
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CardMaker, NodePath

class Narrative(DirectObject.DirectObject):
    def __init__(self, base, gui_node):
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
        self.ui_node = gui_node
        self.base_window = base
        self.art_frame = NodePath()
        self.card = NodePath()
        self.interrupt_flag = False
        #setup
        self.accept('enter', self.page_turn)
        self.accept('space', self.page_turn )