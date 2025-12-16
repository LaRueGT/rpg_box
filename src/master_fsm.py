#panda3d
from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject
#My Stuff
import gui, slideshow, narrative
from src import covermenu

class MasterFSM(FSM, DirectObject):
    def __init__(self, base):
        FSM.__init__(self, 'MasterFSM')
        self.base_window = base
        self.ui = gui.Gui(self.base_window)
        self.request('Intro')

    #state transition event handlers
    def handle_intro_done(self):
        self.request('Narrative')

    #state methods
    def enterIntro(self):
        self.accept('slide_finished', self.handle_intro_done)
        slide_frame = self.ui.centerfold_frame()
        intro = slideshow.Slideshow(self.base_window, slide_frame)
        intro.display_intro_sequence()

    def exitIntro(self):
        self.ignore('escape')
        self.ignore('space')
        self.ui.clear_gui()
        self.ignore('slide_finished')

    def enterCover(self):
        cover_label, cover_button_frame = self.ui.cover_frame()
        cover = covermenu.CoverMenu(self.base_window, cover_label, cover_button_frame)

    def enterNarrative(self):
        narrative_frame, text_label = self.ui.narrative_frame()
        test_narrative = narrative.Narrative(self.base_window, narrative_frame, text_label)
        test_narrative.display_dummy_narrative()

    def exitNarrative(self):
        self.ui.clear_gui()