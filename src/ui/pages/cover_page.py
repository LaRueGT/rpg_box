from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel
from direct.showbase.MessengerGlobal import messenger
import sys

class CoverMenu(DirectObject):
    def __init__(self, base, ui):
        super().__init__()
        #setup
        self.base_window = base
        self.ui = ui
        self.cover_label_frame = DirectFrame(parent=ui.base_frame,
                                             frameColor=(.25, .25, .25, 1),
                                             frameSize=(-1.715, 1.715, -.88, .94))
        self.cover_label = DirectLabel(parent=self.cover_label_frame,
                                       text="Initial Text", text_font=ui.label_font,
                                       text_scale=(0.1, 0.1), pos=(0, 0, 0))
        self.button_frame = ui.make_button_row()
        self.accept('p', self.handle_play_button)
        self.accept('d', self.handle_demo_button)
        self.accept('q', self.handle_quit_button)
        self.accept('escape', self.handle_quit_button)

    #button handlers
    def handle_play_button(self):
        messenger.send('play_button_pressed')

    def handle_demo_button(self):
        self.ignore('d')
        messenger.send('demo_button_pressed')

    def handle_quit_button(self):
        self.ignore('q')
        sys.exit(0)

    def display_cover_menu(self):
        self.cover_label.setText("RPG Box v0 06/20/2026")
        play_button = DirectButton(parent=self.button_frame, text="Play", scale=.05, command=self.handle_play_button)
        demo_button = DirectButton(parent=self.button_frame, text="Demo", scale=.05, command=self.handle_demo_button)
        quit_button = DirectButton(parent=self.button_frame, text="Quit", scale=.05, command=self.handle_quit_button)
        self.button_frame.addItem(play_button)
        self.button_frame.addItem(demo_button)
        self.button_frame.addItem(quit_button)
