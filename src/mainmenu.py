import sys
from direct.showbase.MessengerGlobal import messenger
from direct.gui.DirectGui import DirectButton
from direct.showbase.DirectObject import DirectObject


class MainMenu(DirectObject):
    def __init__(self, base, label, button_frame):
        super().__init__()
        # setup
        self.base_window = base
        self.cover_label = label
        self.button_frame = button_frame
        self.accept('q', self.handle_quit_button)
        self.accept('escape', self.handle_quit_button)

    # button handlers
    def handle_quit_button(self):
        self.ignore('q')
        sys.exit(0)

    def display_main_menu(self):
        self.cover_label.setText("RPG Box v0 12/22/2025")
        ##column 1
        create_button = DirectButton(parent=self.button_frame, text="Create Character", scale=.05,
                                     command=self.handle_create_button)
        delete_button = DirectButton(parent=self.button_frame, text="Delete Character", scale=.05,
                                     command=self.handle_delete_button)
        modify_button = DirectButton(parent=self.button_frame, text="Modify Character", scale=.05,
                                     command=self.handle_modify_button)
        view_button = DirectButton(parent=self.button_frame, text="View Character", scale=.05,
                                   command=self.handle_view_button)
        play_button = DirectButton(parent=self.button_frame, text="Begin Adventuring", scale=.05,
                                   command=self.handle_play_button)
        ## column 2
        add_button = DirectButton(parent=self.button_frame, text="Add Character", scale=.05,
                                  command=self.handle_add_button)
        remove_button = DirectButton(parent=self.button_frame, text="Remove Character", scale=.05,
                                     command=self.handle_remove_button)
        load_button = DirectButton(parent=self.button_frame, text="Load Saved Game", scale=.05,
                                   command=self.handle_load_button)
        save_button = DirectButton(parent=self.button_frame, text="Save Game", scale=.05,
                                   command=self.handle_save_button)
        quit_button = DirectButton(parent=self.button_frame, text="Quit", scale=.05, command=self.handle_quit_button)
        self.button_frame.addItem(create_button)
        self.button_frame.addItem(delete_button)
        self.button_frame.addItem(modify_button)
        self.button_frame.addItem(view_button)
        self.button_frame.addItem(play_button)
        self.button_frame.addItem(add_button)
        self.button_frame.addItem(remove_button)
        self.button_frame.addItem(load_button)
        self.button_frame.addItem(save_button)
        self.button_frame.addItem(quit_button)
