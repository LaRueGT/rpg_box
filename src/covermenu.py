from direct.gui import DirectGuiGlobals as DGG
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton
from direct.showbase.MessengerGlobal import messenger
from DirectGuiExtension.DirectAutoSizer import DirectAutoSizer
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from panda3d.core import NodePath
import sys

class CoverMenu(DirectObject):
    def __init__(self, base, label, button_frame):
        super().__init__()
        #setup
        self.base_window = base
        self.cover_label = label
        self.button_frame = button_frame
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
        J/22/2025")
        play_button = DirectButton(parent=self.button_frame, text="Play", scale=.05, command=self.handle_play_button)
        demo_button = DirectButton(parent=self.button_frame, text="Demo", scale=.05, command=self.handle_demo_button)
        quit_button = DirectButton(parent=self.button_frame, text="Quit", scale=.05, command=self.handle_quit_button)
        self.button_frame.addItem(play_button)
        self.button_frame.addItem(demo_button)
        self.button_frame.addItem(quit_button)
