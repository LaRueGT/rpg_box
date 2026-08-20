import sys
from direct.showbase.MessengerGlobal import messenger
from direct.gui.DirectGui import DirectButton, DirectLabel
from DirectGuiExtension.DirectGridSizer import DirectGridSizer
from direct.showbase.DirectObject import DirectObject
from model import party


class MainMenu(DirectObject):
    def __init__(self, base, ui, character_list=None):
        super().__init__()
        # setup
        self.base_window = base
        self.ui = ui
        self.text_frame = ui.make_content_frame(frame_color=(0, 1, 1, 1))
        self.cover_label = DirectLabel(parent=self.text_frame, text_font=ui.label_font,
                                       text="", text_scale=(0.065, 0.065),
                                       text_pos=(0, -0.025), pos=(0, 0, 0.35),
                                       frameColor=(0, 0, 0, 0))
        self.party: party.Party = party.Party()
        self.recruitable_characters = character_list if character_list is not None else []
        self.button_frame = DirectGridSizer(numColumns=2, numRows=5,
                                            itemMargin=[0.01, 0.01, 0.01, 0.01],
                                            parent=ui.base_frame,
                                            frameColor=(0, 1, 0, 1),
                                            frameSize=(-1.715, 1.715, -.205, .205),
                                            pos=(0, 0, -0.675))
        self.accept('q', self.handle_quit_button)
        self.accept('escape', self.handle_quit_button)

    # button handlers
    def handle_quit_button(self):
        self.ignore('q')
        sys.exit(0)

    def handle_create_button(self):
        print("create button pressed")
        messenger.send("chargen_button_pressed")

    def handle_delete_button(self):
        print("delete button pressed")
        messenger.send("delete_character_button_pressed")

    def handle_modify_button(self):
        print("modify button pressed")

    def handle_view_button(self):
        print("view button pressed")

    def handle_play_button(self):
        print("play button pressed")

    def handle_assign_party_button(self):
        print("assign party button pressed")
        messenger.send("party_assign_button_pressed")

    def handle_load_button(self):
        print("load button pressed")

    def handle_save_button(self):
        print("save button pressed")


    def display_main_menu(self):
        self.update_party_display()
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
        assign_party_button = DirectButton(
            parent=self.button_frame, text="Assign Party", scale=.05,
            command=self.handle_assign_party_button)
        load_button = DirectButton(parent=self.button_frame, text="Load Saved Game", scale=.05,
                                   command=self.handle_load_button)
        save_button = DirectButton(parent=self.button_frame, text="Save Game", scale=.05,
                                   command=self.handle_save_button)
        quit_button = DirectButton(parent=self.button_frame, text="Quit", scale=.05, command=self.handle_quit_button)
        self.button_frame.addItem(create_button, 0, 0)
        self.button_frame.addItem(delete_button, 1, 0)
        self.button_frame.addItem(modify_button, 2, 0)
        self.button_frame.addItem(view_button, 3, 0)
        self.button_frame.addItem(play_button, 4, 0)
        self.button_frame.addItem(assign_party_button, 0, 1)
        self.button_frame.addItem(load_button, 1, 1)
        self.button_frame.addItem(save_button, 2, 1)
        self.button_frame.addItem(quit_button, 3, 1)

    def update_party_display(self):
        """Refresh the party summary shown in the main-menu content frame."""
        heading = "{:<24}{}".format("Name", "Max HP")
        members = "\n".join(
            "{:<24}{}".format(member.name, member.max_hp)
            for member in self.party.members
        )
        party_text = "Party Members\n\n" + heading
        self.cover_label['text'] = party_text + ("\n" + members if members else "\n(None selected)")
