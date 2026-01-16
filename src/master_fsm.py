#panda3d
#python
import sys

from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject

import chargen
import chargen_p2
import covermenu

#My Stuff
import gui
import mainmenu
import narrative
import slideshow

#NB: FSM uses non-snake function naming with (enterState, exitState, filterState)
#NB:

class MasterFSM(FSM, DirectObject):
    def __init__(self, base):
        FSM.__init__(self, 'MasterFSM')
        self.base_window = base
        self.ui = gui.Gui(self.base_window)
        self.chargen_screen = None
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

    def handle_chargen_done(self):
        self.request('Main')

    def main_chargen(self):
        self.request('Chargen')

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
        cover = covermenu.CoverMenu(self.base_window, cover_label, cover_button_frame)
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
        test_narrative = narrative.Narrative(self.base_window, narrative_frame, text_label)
        test_narrative.display_dummy_narrative()

    def exitDemo(self):
        self.ignore('escape')
        self.ignore('space')
        self.ignore('demo_finished')
        self.ui.clear_gui()

    def enterMain(self):
        self.accept('main_finished', self.handle_main_done)
        self.accept('chargen_button_pressed', self.main_chargen)
        party_label, button_grid = self.ui.main_frame()
        main_menu = mainmenu.MainMenu(self.base_window, party_label, button_grid)
        main_menu.display_main_menu()

    def exitMain(self):
        self.ignore('escape')
        self.ignore('space')
        self.ignore('main_finished')
        self.ui.clear_gui()

    def enterChargen(self):
        self.accept('chargen_continue', self.handle_chargen_continue)
        ability_label, race_list, alignment_list, gender_list, class_list, button_row = self.ui.chargen_frame()
        self.chargen_screen = chargen.Chargen(self.base_window, ability_label,race_list, alignment_list, gender_list,class_list,button_row)
        self.chargen_screen.display_chargen_buttons()
        self.chargen_screen.display_race_picker()
        self.chargen_screen.display_alignment_picker()
        self.chargen_screen.display_gender_picker()
        self.chargen_screen.display_class_picker()

    def exitChargen(self):
        self.ignore('escape')
        self.ignore('chargen_finished')
        self.ui.clear_gui()

    def enterChargenP2(self):
        character_data = self.chargen_screen.new_char
        self.accept('chargenp2_finished', self.handle_chargen_done)
        self.accept('chargen_cancel', self.handle_chargen_cancel)
        ability_frame, button_frame = self.ui.chargenp2_frame()
        modifiers_label = self.ui.modifiers_label
        attacks_label = self.ui.attack_values_label
        chargen_pg2 = chargen_p2.Chargen_p2(self.base_window, ability_frame, button_frame, character_data, modifiers_label, attacks_label)
        chargen_pg2.display_adjustment_boxes()
        chargen_pg2.display_chargen_buttons()

    def exitChargenP2(self):
        self.ignore('escape')
        self.ignore('chargenp2_finished')
        self.ignore('chargen_cancel')
        self.ui.clear_gui()