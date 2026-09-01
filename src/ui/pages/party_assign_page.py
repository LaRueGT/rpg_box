from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton, DirectCheckButton
from direct.gui.DirectGui import DirectFrame, DirectLabel
from DirectGuiExtension.DirectGridSizer import DirectGridSizer
from direct.showbase.MessengerGlobal import messenger
from rules.party_rules import PartyRules


class PartyAssign(DirectObject):
    def __init__(
        self, base, ui, character_list, party_obj
    ):
        super().__init__()
        self.base_window = base
        self.ui = ui
        self.cover_label_frame = DirectFrame(parent=ui.base_frame,
                                             frameColor=(.25, .25, .25, 1),
                                             frameSize=ui.SAFE)
        self.label = DirectLabel(parent=self.cover_label_frame,
                                 text="Select up to 6 Characters",
                                 text_font=ui.label_font, text_scale=(ui.TITLE, ui.TITLE),
                                 text_fg=ui.GOLD, text_align=2, pos=(0, 0, 0.72),
                                 frameColor=(0, 0, 0, 0))
        self.list_frame = DirectGridSizer(
                                          numColumns=3,
                                          numRows=max(1, (len(character_list) + 2) // 3),
                                          parent=self.cover_label_frame,
                                          frameColor=(0, 0, 0, 0), pos=(0, 0, 0.6))
        self.button_frame = ui.make_button_row()
        self.party_rules = PartyRules(character_list, party_obj)
        self.check_buttons = {}

    def display_party_assign(self):
        # Clear previous frame if necessary
        for i, char in enumerate(self.party_rules.available_characters):
            is_in_party = self.party_rules.is_selected(char)

            cb = DirectCheckButton(
                parent=self.list_frame,
                text=char.name,
                scale=self.ui.BUTTON, text_font=self.ui.label_font,
                indicatorValue=is_in_party,
                command=self.handle_check,
                extraArgs=[char],
            )
            self.list_frame.addItem(cb, i // 3, i % 3)
            self.check_buttons[char] = cb

        back_button = DirectButton(
            parent=self.button_frame,
            text="[B] Back to Menu",
            scale=self.ui.BUTTON, text_font=self.ui.label_font,
            command=self.handle_back,
        )
        self.button_frame.addItem(back_button)

    def handle_check(self, status, char):
        accepted = self.party_rules.set_selected(char, status)
        if not accepted:
            self.check_buttons[char]['indicatorValue'] = False

    def handle_back(self):
        self.party_rules.apply_to_party()
        messenger.send("main_menu_requested")
