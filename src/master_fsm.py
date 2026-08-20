#panda3d
#python
import sys

from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject

from ui import gui

from ui.pages import chargen_page
from ui.pages import cover_page
from ui.pages import main_menu_page
from ui.pages import narrative_page
from ui.pages import party_assign_page
from ui.pages import slideshow
from model import party

#NB: Panda3d FSM uses non-snake function naming with (enterState, exitState, filterState)

class MasterFSM(FSM, DirectObject):
    def __init__(self, base):
        FSM.__init__(self, 'MasterFSM')
        self.base_window = base
        self.ui = gui.Gui(self.base_window)
        self.chargen_screen = None
        self.main_menu = None
        self.character_list = []
        self.adventure_party = party.Party()
        self.request('Intro')

    #state transition event handlers
    def handle_intro_done(self):
        self.request('Cover')

    def handle_demo_done(self):
        self.request('Cover')

    def cover_play(self):
        self.request('Main')

    def cover_demo(self):
        self.request('Demo')

    def handle_chargen_continue(self):
        self.request('ChargenP2')

    def handle_chargen_cancel(self):
        self.request('Main')

    def handle_chargen_done(self, character_obj):
        print(f"Adding {character_obj.name} to recruitable list")
        self.character_list.append(character_obj)
        self.request('Main')

    def main_chargen(self):
        self.request('Chargen')

    def main_party_assign(self):
        self.request('Party')

    def handle_main_done(self):
        sys.exit(0)

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
        cover = cover_page.CoverMenu(self.base_window, cover_label, cover_button_frame)
        cover.display_cover_menu()

    def exitCover(self):
        self.ignore('p')
        self.ignore('d')
        self.ignore('q')
        self.ignore('play_button_pressed')
        self.ignore('demo_button_pressed')
        self.ui.clear_gui()

    def enterDemo(self):
        self.accept('demo_finished', self.handle_intro_done)
        narrative_frame, text_label = self.ui.narrative_frame()
        test_narrative = narrative_page.Narrative(self.base_window, narrative_frame, text_label)
        test_narrative.display_dummy_narrative()

    def exitDemo(self):
        self.ignore('escape')
        self.ignore('space')
        self.ignore('demo_finished')
        self.ui.clear_gui()

    def enterMain(self):
        self.accept('main_finished', self.handle_main_done)
        self.accept('chargen_button_pressed', self.main_chargen)
        self.accept('party_assign_button_pressed', self.main_party_assign)
        party_label, button_grid = self.ui.main_frame()
        self.main_menu = main_menu_page.MainMenu(self.base_window, party_label, button_grid, self.character_list)
        self.main_menu.party = self.adventure_party
        self.main_menu.display_main_menu()

    def exitMain(self):
        self.ignore('escape')
        self.ignore('space')
        self.ignore('main_finished')
        self.ignore('chargen_button_pressed')
        self.ignore('party_assign_button_pressed')
        self.ui.clear_gui()

    def enterChargen(self):
        self.accept('chargen_continue', self.handle_chargen_continue)
        self.accept("chargen_cancel", self.handle_chargen_cancel)
        screen_frame, button_frame = self.ui.chargen_frame()
        self.chargen_screen = chargen_page.Chargen(self.base_window, screen_frame, button_frame)
        self.chargen_screen.display_first_page()

    def exitChargen(self):
        self.ignore('escape')
        self.ignore("chargen_continue")
        self.ignore("chargen_cancel")
        self.ui.clear_gui()

    def enterChargenP2(self):
        character_data = self.chargen_screen.new_char
        self.accept("chargen_done", self.handle_chargen_done)
        self.accept('chargen_cancel', self.handle_chargen_cancel)
        screen_frame, button_frame = self.ui.chargen_frame()
        self.chargen_screen = chargen_page.Chargen(
            self.base_window, screen_frame, button_frame, character_data
        )
        self.chargen_screen.display_second_page()

    def exitChargenP2(self):
        self.ignore('escape')
        self.ignore('chargen_done')
        self.ignore('chargen_cancel')
        self.ui.clear_gui()

    def enterParty(self):
        party_label, box_frame, button_frame = self.ui.party_assign_frame()
        party_page = party_assign_page.PartyAssign(self.base_window, party_label, box_frame, button_frame, self.character_list,
                                                   self.adventure_party)
        party_page.display_party_assign()

    def exitParty(self):
        self.ui.clear_gui()
