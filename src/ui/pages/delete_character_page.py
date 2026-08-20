from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton, DirectCheckButton
from direct.gui.DirectGui import DirectFrame, DirectLabel
from DirectGuiExtension.DirectGridSizer import DirectGridSizer
from direct.showbase.MessengerGlobal import messenger


class DeleteCharacter(DirectObject):
    """Page for selecting and deleting characters outside the active party."""

    def __init__(self, base, ui, character_list, party_obj):
        super().__init__()
        self.base_window = base
        self.ui = ui
        self.available_characters = [
            character for character in character_list
            if character not in party_obj.members
        ]
        self.selected_characters = set()
        self.check_buttons = {}

        self.page_frame = DirectFrame(
            parent=ui.base_frame,
            frameColor=(.25, .25, .25, 1),
            frameSize=(-1.715, 1.715, -.88, .94),
        )
        self.label = DirectLabel(
            parent=self.page_frame,
            text="Select Characters to Delete",
            text_font=ui.label_font,
            text_scale=(0.1, 0.1),
            pos=(0, 0, 0.8),
        )
        self.list_frame = DirectGridSizer(
            numColumns=3,
            numRows=max(1, (len(self.available_characters) + 2) // 3),
            parent=self.page_frame,
            frameColor=(0, 0, 0, 0),
            pos=(0, 0, 0.6),
        )
        self.button_frame = ui.make_button_row()

    def display_delete_characters(self):
        for index, character in enumerate(self.available_characters):
            check_button = DirectCheckButton(
                parent=self.list_frame,
                text=character.name,
                scale=0.05,
                command=self.handle_check,
                extraArgs=[character],
            )
            self.list_frame.addItem(check_button, index // 3, index % 3)
            self.check_buttons[character] = check_button

        delete_button = DirectButton(
            parent=self.button_frame,
            text="Delete Selected",
            scale=0.05,
            command=self.handle_delete,
        )
        back_button = DirectButton(
            parent=self.button_frame,
            text="Back to Menu",
            scale=0.05,
            command=self.handle_back,
        )
        self.button_frame.addItem(delete_button)
        self.button_frame.addItem(back_button)

    def handle_check(self, status, character):
        if status:
            self.selected_characters.add(character)
        else:
            self.selected_characters.discard(character)

    def handle_delete(self):
        messenger.send(
            "delete_characters_requested",
            [list(self.selected_characters)],
        )

    def handle_back(self):
        messenger.send("main_menu_requested")
