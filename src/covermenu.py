from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from panda3d.core import NodePath

class CoverMenu(DirectObject):
    def __init__(self, base, label, buttonframe):
        super().__init__()
        self.label = NodePath()
        #setup
        self.base_window = base
        self.cover_label = label
        self.button_frame = buttonframe
        self.accept('p', self.handle_play_button)
        self.accept('d', self.handle_demo_button)
        self.accept('q', self.handle_quit)
        self.accept('escape', self.handle_quit)

    #button handlers
    def handle_play_button(self):
        messenger.send('play_button_pressed')
        self.ignore('p')

    def handle_demo_button(self):
        messenger.send('demo_button_pressed')
        self.ignore('d')

    def display_cover_menu(self):
        self.label.setText("RPG Box v0 11/7/2025")