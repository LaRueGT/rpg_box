#panda3d
from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject
#My Stuff
import gui, slideshow, narrative

class MasterFSM(FSM, DirectObject):
    def __init__(self, base):
        FSM.__init__(self, 'MasterFSM')
        self.base_window = base
        self.ui = gui.Gui(self.base_window)
        self.request('Intro')

    #event handlers
    def handle_intro_done(self):
        self.request('Narrative')

    #state methods
    def enterIntro(self):
        self.accept('slide_finished', self.handle_intro_done)
        slide_frame = self.ui.centerfold_frame()
        intro = slideshow.Slideshow(self.base_window, slide_frame)
        intro.display_intro_sequence()

    def exitIntro(self):
        self.ui.clear_gui()
        self.ignore('slide_finished')

    def enterNarrative(self):
        narrative_frame, text_label = self.ui.narrative_frame()
        testnarrative = narrative.Narrative(self.base_window, narrative_frame, text_label)
        testnarrative.display_dummy_narrative()

    def exitNarrative(self):
        self.ui.clear_gui()