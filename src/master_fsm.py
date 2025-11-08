#panda3d
from direct.fsm.FSM import FSM
#My Stuff
import gui, slideshow, narrative

class MasterFSM(FSM):
    def __init__(self, base):
        FSM.__init__(self, 'MasterFSM')
        self.base_window = base
        self.ui = gui.Gui(self.base_window)

    def enterIntro(self):
        slide_frame = self.ui.centerfold_frame()
        intro = slideshow.Slideshow(self.base_window, slide_frame)
        intro.display_intro_sequence()

    def exitIntro(self):
        self.ui.clear_gui()

    def enterNarrative(self):
        narrative_frame, text_label = self.ui.narrative_frame()
        testnarrative = narrative.Narrative(self, narrative_frame, text_label)
        testnarrative.display_dummy_narrative()

    def exitNarrative(self):
        self.ui.clear_gui()