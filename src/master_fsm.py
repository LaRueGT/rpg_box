#panda3d
from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject
#My Stuff
import gui
import narrative
import slideshow
import covermenu

#NB: FSM uses non-snake function naming with (enterState, exitState, filterState)
#NB:

class MasterFSM(FSM, DirectObject):
    def __init__(self, base):
        FSM.__init__(self, 'MasterFSM')
        self.base_window = base
        self.ui = gui.Gui(self.base_window)
        self.request('Intro')

    #state transition event handlers
    def handle_intro_done(self):
        self.request('Cover')

    def cover_play(self):
        self.request('MainMenu')

    def cover_demo(self):
        self.request('Narrative')

    #state methods
    def enterIntro(self):
        self.accept('slides_finished', self.handle_intro_done)
        slide_frame = self.ui.centerfold_frame()
        intro = slideshow.Slideshow(self.base_window, slide_frame)
        intro.display_intro_sequence()

    def exitIntro(self):
        self.ignore('escape')
        self.ignore('space')
        self.ignore('slides_finished')
        self.ui.clear_gui()

    def enterCover(self):
        self.accept('play_button_pressed', self.cover_play)
        self.accept('demo_button_pressed', self.cover_demo)
        cover_label, cover_button_frame = self.ui.cover_frame()
        cover = covermenu.CoverMenu(self.base_window, cover_label, cover_button_frame)
        cover.display_cover_menu()

    def exitCover(self):
        self.ignore('p')
        self.ignore('d')
        self.ignore('q')
        self.ignore('play_button_pressed')
        self.ignore('demo_button_pressed')
        self.ui.clear_gui()

    def enterNarrative(self):
        narrative_frame, text_label = self.ui.narrative_frame()
        test_narrative = narrative.Narrative(self.base_window, narrative_frame, text_label)
        test_narrative.display_dummy_narrative()

    def exitNarrative(self):
        self.ui.clear_gui()