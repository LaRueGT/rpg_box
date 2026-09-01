"""Character sheet display used by the main-menu View Character action."""

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from panda3d.core import TextNode

from rules import ability_rules, leveling_rules
from rules.character_creation import ABILITY_ATTRS


class CharacterSheet(DirectObject):
    """Display the currently selected character and allow switching characters."""

    SAVE_LABELS = (
        ("death_poison", "Death / Poison"),
        ("wands", "Wands"),
        ("paralysis_petrify", "Paralysis / Petrify"),
        ("breath", "Breath"),
        ("spells_rods_staves", "Spells / Rods / Staves"),
    )

    def __init__(self, base, ui, character_list):
        super().__init__()
        self.base_window = base
        self.ui = ui
        self.characters = list(character_list)
        self.selected_character = self.characters[0] if self.characters else None

        self.page_frame = ui.make_grid_paper_page()
        # Light panels echo the reference sheet while keeping the graph-paper
        # page visible. Labels stay parented to page_frame; see _make_label.
        self._make_panel((-1.20, -.03, .22, .55))
        self._make_panel((.03, 1.20, .22, .55))
        self._make_panel((-1.20, -.03, -.62, .16))
        self._make_panel((.03, 1.20, -.62, .16))
        self.button_frame = ui.make_button_row(frame_color=(0, 0, 0, 0))
        self.title_label = self._make_label(self.page_frame, ui.TITLE, (-1.12, 0, .78))
        self.combat_label = self._make_label(self.page_frame, ui.SMALL, (-1.12, 0, .48))
        self.ability_label = self._make_label(self.page_frame, ui.SMALL, (.11, 0, .48))
        self.inventory_label = self._make_label(self.page_frame, ui.SMALL, (-1.12, 0, .14))
        self.saving_label = self._make_label(self.page_frame, ui.SMALL, (.11, 0, .14))
        self.future_label = self._make_label(self.page_frame, ui.SMALL, (.11, 0, -.45))
        self.accept("escape", self.handle_back)

    def display_character_sheet(self):
        """Create the picker and render the first available character."""
        DirectLabel(
            parent=self.page_frame, text="View Character:",
            text_font=self.ui.label_font, text_scale=self.ui.BODY,
            pos=(-1.12, 0, .64), frameColor=(0, 0, 0, 0),
        )
        for index, character in enumerate(self.characters):
            button = DirectButton(
                parent=self.page_frame, text=character.name or "Unnamed",
                text_font=self.ui.label_font, scale=self.ui.BUTTON,
                pos=(-.74 + index * .42, 0, .65),
                command=self.select_character, extraArgs=[character],
            )
            # Keep the buttons visible even when there are more characters than
            # fit on the first row; this is primarily a small-party interface.
            if index >= 6:
                button.setZ(.65 - ((index - 5) // 6) * .1)

        back_button = DirectButton(
            parent=self.button_frame, text="[B] Back to Menu", scale=self.ui.BUTTON,
            text_font=self.ui.label_font, command=self.handle_back,
        )
        self.button_frame.addItem(back_button)
        items_button = DirectButton(
            parent=self.button_frame, text="[M] Manage Items", scale=self.ui.BUTTON,
            text_font=self.ui.label_font, command=self.handle_items,
        )
        self.button_frame.addItem(items_button)
        self.refresh_sheet()

    def _make_panel(self, frame_size):
        DirectFrame(
            parent=self.page_frame, frameColor=(1, 1, 1, .28),
            frameSize=frame_size, pos=(0, 0, 0),
        )

    def _make_label(self, parent, scale, pos):
        return DirectLabel(
            parent=parent, text="", text_font=self.ui.label_font,
            text_scale=(scale, scale),
            text_align=TextNode.ALeft, text_pos=(0, 0), pos=pos,
            frameColor=(0, 0, 0, 0),
        )

    def select_character(self, character):
        self.selected_character = character
        self.refresh_sheet()

    def refresh_sheet(self):
        character = self.selected_character
        if character is None:
            self.title_label["text"] = "CHARACTER SHEET"
            self.combat_label["text"] = "No characters have been created yet."
            self.ability_label["text"] = ""
            self.inventory_label["text"] = ""
            self.saving_label["text"] = ""
            self.future_label["text"] = ""
            return

        # Characters created by the current chargen flow already have these
        # values. Recalculate saves here as a safe fallback for older objects.
        if character.char_classes:
            leveling_rules.update_saving_throws(character)

        abilities = self._ability_lines(character)
        saves = self._saving_throw_lines(character)
        classes = ", ".join(str(value) for value in character.char_classes) or "None"
        levels = ", ".join(str(value) for value in character.level) or "1"
        race = str(character.char_race) if character.char_race else "-"
        alignment = str(character.char_alignment) if character.char_alignment else "-"
        ac = character.armor_class

        self.title_label["text"] = f"{character.name or 'Unnamed'}    {race}    {alignment}"
        self.combat_label["text"] = (
            f"Class: {classes}    Level: {levels}\n"
            "COMBAT\n"
            f"HP: {character.max_hp}\n"
            f"Armor Class: {ac} (descending)\n"
            f"THAC0: {character.thaco}\n"
            f"Melee Attack Bonus: {self._modifier(character.strength)}\n"
            f"Missile Attack Bonus: {self._modifier(character.dexterity)}"
        )
        self.ability_label["text"] = "ABILITY SCORES\n" + abilities
        self.saving_label["text"] = "SAVING THROWS\n" + saves
        self.inventory_label["text"] = (
            "EQUIPMENT\n"
            + self._equipment_lines(character) + "\n\n"
            "MONEY / ENCUMBRANCE\n"
            f"{character.encumbrance}/{character.carrying_capacity} coins\n"
            f"Movement: {character.movement_rate}"
        )
        self.future_label["text"] = (
            "FUTURE FEATURES\n"
            "Skills, weapons, portrait\n"
            "Not implemented"
        )

    @staticmethod
    def _equipment_lines(character):
        return "\n".join(
            f"{slot.value.replace('_', ' '):<12}: {item.name if item else '-'}"
            for slot, item in character.inventory.equipped.items()
        )

    @staticmethod
    def _modifier(score):
        try:
            value = ability_rules.ability_modifier(score)
        except (TypeError, ValueError):
            return "-"
        return f"{value:+d}"

    @classmethod
    def _armor_class(cls, character):
        try:
            return ability_rules.armor_class(character.dexterity)
        except (TypeError, ValueError):
            return "-"

    @classmethod
    def _ability_lines(cls, character):
        return "\n".join(
            f"{name[:3].upper():<4} {getattr(character, attr):>2}  {cls._modifier(getattr(character, attr)):>2}"
            for name, attr in ABILITY_ATTRS.items()
        )

    @staticmethod
    def _saving_throw_lines(character):
        return "\n".join(
            f"{label:<24} {character.saving_throws.get(key, '-') or '-'}"
            for key, label in CharacterSheet.SAVE_LABELS
        )

    def handle_back(self):
        self.ignore("escape")
        messenger.send("main_menu_requested")

    def handle_items(self):
        messenger.send("item_management_requested")
