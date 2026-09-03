import sys
from direct.showbase.MessengerGlobal import messenger
from direct.gui.DirectGui import DirectButton, DirectLabel
from DirectGuiExtension.DirectGridSizer import DirectGridSizer
from direct.showbase.DirectObject import DirectObject
from model import party
from rules import ability_rules
from panda3d.core import TextNode


class MainMenu(DirectObject):
    def __init__(self, base, ui, character_list=None):
        super().__init__()
        # setup
        self.base_window = base
        self.ui = ui
        self.text_frame = ui.make_content_frame(frame_color=ui.PANEL,
                                                frame_size=(-1.08, 1.08, -.55, .70))
        self.cover_label = DirectLabel(parent=self.text_frame, text_font=ui.label_font,
                                       text="", text_scale=(ui.BODY, ui.BODY),
                                       text_fg=ui.PAPER, text_align=TextNode.ALeft,
                                       text_pos=(-.95, -.02), pos=(0, 0, 0.50),
                                       frameColor=(0, 0, 0, 0))
        self.party: party.Party = party.Party()
        self.recruitable_characters = character_list if character_list is not None else []
        self.button_frame = DirectGridSizer(numColumns=2, numRows=5,
                                            itemMargin=[0.01, 0.01, 0.01, 0.01],
                                            parent=ui.base_frame,
                                            frameColor=(0, 0, 0, 0),
                                            frameSize=(-1.12, 1.12, -.16, .16),
                                            pos=(0, 0, -0.18), pad=(-.70, 0), boxAlign=TextNode.ACenter,
                                            autoUpdateFrameSize=False)
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
        messenger.send("view_character_button_pressed")

    def handle_play_button(self):
        print("play button pressed")
        if self.party.members:
            messenger.send("begin_adventuring_button_pressed")
        else:
            self.cover_label["text"] = "Party Members\n\nAssign at least one character before beginning an adventure."

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
        create_button = DirectButton(parent=self.button_frame, text="[C] Create Character", text_font=self.ui.label_font, scale=self.ui.BUTTON,
                                     command=self.handle_create_button)
        delete_button = DirectButton(parent=self.button_frame, text="[D] Delete Character", text_font=self.ui.label_font, scale=self.ui.BUTTON,
                                     command=self.handle_delete_button)
        modify_button = DirectButton(parent=self.button_frame, text="[M] Modify Character", text_font=self.ui.label_font, scale=self.ui.BUTTON,
                                     command=self.handle_modify_button)
        view_button = DirectButton(parent=self.button_frame, text="[V] View Character", text_font=self.ui.label_font, scale=self.ui.BUTTON,
                                   command=self.handle_view_button)
        play_button = DirectButton(parent=self.button_frame, text="[B] Begin Adventuring", text_font=self.ui.label_font, scale=self.ui.BUTTON,
                                   command=self.handle_play_button)
        ## column 2
        assign_party_button = DirectButton(
            parent=self.button_frame, text="[A] Assign Party", text_font=self.ui.label_font, scale=self.ui.BUTTON,
            command=self.handle_assign_party_button)
        load_button = DirectButton(parent=self.button_frame, text="[L] Load Saved Game", text_font=self.ui.label_font, scale=self.ui.BUTTON,
                                   command=self.handle_load_button)
        save_button = DirectButton(parent=self.button_frame, text="[S] Save Game", text_font=self.ui.label_font, scale=self.ui.BUTTON,
                                   command=self.handle_save_button)
        quit_button = DirectButton(parent=self.button_frame, text="[Q] Quit", text_font=self.ui.label_font, scale=self.ui.BUTTON, command=self.handle_quit_button)
        # Fixed cells keep both columns aligned regardless of label length.
        for button in (create_button, delete_button, modify_button, view_button,
                       play_button, assign_party_button, load_button, save_button,
                       quit_button):
            button['frameSize'] = (-7.0, 7.0, -1.35, 1.35)
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
        heading = "{:<24}{:>4}{:>8}".format("Name", "AC", "Max HP")
        members = "\n".join(
            "{:<24}{:>4}{:>8}".format(
                member.name,
                self._armor_class(member),
                member.max_hp,
            )
            for member in self.party.members
        )
        party_text = "Party Members\n\n" + heading
        self.cover_label['text'] = party_text + ("\n" + members if members else "\n(None selected)")

    @staticmethod
    def _armor_class(character):
        try:
            return ability_rules.armor_class(character.dexterity)
        except (AttributeError, TypeError, ValueError):
            return "-"
