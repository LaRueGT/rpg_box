from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectButton, DirectCheckButton
from direct.showbase.MessengerGlobal import messenger


class PartyAssign(DirectObject):
    def __init__(
        self, base, label, list_frame, button_frame, character_list, party_obj
    ):
        super().__init__()
        self.base_window = base
        self.label = label
        self.list_frame = list_frame
        self.button_frame = button_frame
        self.character_list = character_list
        self.party = party_obj
        self.selections = {}

    def display_party_assign(self):
        # Clear previous frame if necessary
        for i, char in enumerate(self.character_list):
            # Check if character is already in party
            is_in_party = char in self.party.members

            cb = DirectCheckButton(
                parent=self.list_frame,
                text=char.name,
                scale=0.05,
                indicatorValue=is_in_party,
                command=self.handle_check,
                extraArgs=[char],
            )
            self.list_frame.addItem(cb)
            self.selections[char] = is_in_party

        back_button = DirectButton(
            parent=self.button_frame,
            text="Back to Menu",
            scale=0.05,
            command=self.handle_back,
        )
        self.button_frame.addItem(back_button)

    def handle_check(self, status, char):
        selected_count = sum(1 for val in self.selections.values() if val)

        if status and selected_count >= 6:
            # Revert check if already at 6
            self.refresh_ui()
            return

        self.selections[char] = bool(status)

    def handle_back(self):
        # Update the party object with new selections
        self.party.members = [
            char for char, selected in self.selections.items() if selected
        ]
        messenger.send("main_menu_requested")

    def refresh_ui(self):
        # Implementation to force UI update if limit exceeded
        messenger.send("party_assign_button_pressed")
