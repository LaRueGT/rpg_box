"""Rules for choosing the characters that make up the active party."""
from model.character import Character
from model.party import Party


class PartyRules:
    """Keep party selection state separate from the party-assignment UI."""
    MAX_PARTY_SIZE = 6

    def __init__(
        self,
        available_characters: list[Character],
        party: Party,
        max_party_size: int = MAX_PARTY_SIZE,
    ):
        self.available_characters = list(available_characters)
        self.party = party
        self.max_party_size = max_party_size
        self._selected = {
            character: character in party.members
            for character in self.available_characters
        }

        # A party loaded from elsewhere should not make the assignment screen
        # exceed its limit.
        selected = [
            character for character in self.available_characters
            if self._selected[character]
        ]
        for character in selected[self.max_party_size:]:
            self._selected[character] = False

    @property
    def selected_characters(self) -> list[Character]:
        return [
            character for character in self.available_characters
            if self._selected[character]
        ]

    @property
    def selected_count(self) -> int:
        return len(self.selected_characters)

    def is_selected(self, character: Character) -> bool:
        return self._selected.get(character, False)

    def set_selected(self, character: Character, selected: bool) -> bool:
        """Set a character's selection, returning whether the change was kept."""
        if character not in self._selected:
            return False

        if selected and not self._selected[character]:
            if self.selected_count >= self.max_party_size:
                return False

        self._selected[character] = bool(selected)
        return True

    def apply_to_party(self) -> None:
        """Commit the current selection to the model when leaving the page."""
        self.party.members = self.selected_characters
