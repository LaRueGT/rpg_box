"""DirectGUI item manager; game decisions remain in rules modules."""

from direct.gui.DirectGui import DirectButton, DirectLabel
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from model.item import EquipmentSlot, Item, ItemType
from rules.equipment_rules import (
    EquipmentError,
    drop_item,
    equip_item,
    transfer_item,
    validate_encumbrance,
)


class ItemManagement(DirectObject):
    SHOP_ITEMS = (
        Item("Dagger", 10, 3, ItemType.WEAPON),
        Item("Sword", 60, 10, ItemType.WEAPON),
        Item("Two-handed sword", 150, 15, ItemType.WEAPON, two_handed=True),
        Item("Leather", 200, 20, ItemType.ARMOR),
        Item("Chainmail", 400, 75, ItemType.ARMOR),
        Item("Plate mail", 500, 60, ItemType.ARMOR),
        Item("Shield", 100, 10, ItemType.SHIELD),
        Item("Ring of protection", 1, 100, ItemType.RING, {"AC": -1}),
        Item(
            "Backpack",
            20,
            5,
            ItemType.MISC,
            container_capacity=400,
            container_size="small",
        ),
    )

    def __init__(self, base, ui, characters):
        super().__init__()
        self.base_window, self.ui = base, ui
        self.characters = list(characters)
        self.selected_character = self.characters[0] if self.characters else None
        self.page_frame = ui.make_grid_paper_page()
        self.content = ui.make_content_frame(
            frame_color=(0, 0, 0, 0.78), frame_size=(-1.6, 1.6, -0.72, 0.82)
        )
        self.status = DirectLabel(
            parent=self.content,
            text="",
            text_font=ui.label_font,
            text_scale=0.04,
            pos=(-1.48, 0, 0.68),
            frameColor=(0, 0, 0, 0),
        )
        self.buttons = ui.make_button_row(frame_color=(0, 0, 0, 0))
        self.accept("escape", self.handle_back)

    def display(self):
        self.refresh()

    def refresh(self):
        for child in list(self.content.getChildren()):
            if child != self.status.node():
                child.removeNode()
        char = self.selected_character
        if char is None:
            self.status["text"] = "No characters available."
            return
        lines = [
            f"{char.name or 'Unnamed'}  ITEM MANAGEMENT",
            "",
            "Item                         Location",
        ]
        lines += [
            f"{i.name[:27]:<27} {char.inventory.location_of(i)}" for i in char.inventory
        ]
        lines += [
            "",
            f"Encumbrance: {char.encumbrance}/{char.carrying_capacity} coins",
            f"Movement: {char.movement_rate}",
        ]
        self.status["text"] = "\n".join(lines)
        for index, item in enumerate(char.inventory.items):
            y = 0.27 - index * 0.065
            self._button(f"Equip {item.name}", self.handle_equip, item).setPos(
                -0.7, 0, y
            )
            self._button("Drop", self.handle_drop, item).setPos(0.35, 0, y)
            if len(self.characters) > 1:
                self._button("Give", self.handle_transfer, item).setPos(0.62, 0, y)
        DirectLabel(
            parent=self.content,
            text="TEST SHOP",
            text_font=self.ui.label_font,
            text_scale=0.04,
            pos=(-1.45, 0, -0.54),
            frameColor=(0, 0, 0, 0),
        )
        for index, item in enumerate(self.SHOP_ITEMS):
            self._button(f"Take {item.name}", self.handle_shop, item).setPos(
                -0.75 + (index % 3) * 0.55, 0, -0.62 - (index // 3) * 0.065
            )
        back = DirectButton(
            parent=self.buttons,
            text="Back",
            scale=0.055,
            text_font=self.ui.label_font,
            command=self.handle_back,
        )
        self.buttons.addItem(back)

    def _button(self, text, command, item):
        return DirectButton(
            parent=self.content,
            text=text,
            scale=0.035,
            text_font=self.ui.label_font,
            command=command,
            extraArgs=[item],
        )

    def _message(self, text):
        self.status["text"] = text

    def handle_equip(self, item):
        slots = {
            ItemType.WEAPON: EquipmentSlot.MAIN_HAND,
            ItemType.ARMOR: EquipmentSlot.BODY_ARMOR,
            ItemType.SHIELD: EquipmentSlot.OFF_HAND,
            ItemType.RING: EquipmentSlot.RING_1,
        }
        try:
            equip_item(self.selected_character, item, slots[item.item_type])
            self.refresh()
        except (EquipmentError, KeyError) as exc:
            self._message(str(exc))

    def handle_drop(self, item):
        drop_item(self.selected_character, item)
        self.refresh()

    def handle_transfer(self, item):
        target = next(
            (c for c in self.characters if c is not self.selected_character), None
        )
        if target:
            try:
                transfer_item(self.selected_character, target, item)
                self.refresh()
            except EquipmentError as exc:
                self._message(str(exc))

    def handle_shop(self, template):
        item = Item(
            template.name,
            template.weight,
            template.gold_value,
            template.item_type,
            dict(template.stat_modifiers),
            template.quantity,
            template.two_handed,
            template.container_capacity,
            template.container_size,
        )
        try:
            self.selected_character.inventory.add(item)
            validate_encumbrance(self.selected_character)
            self.refresh()
        except (ValueError, EquipmentError) as exc:
            self._message(str(exc))

    def handle_back(self):
        self.ignore("escape")
        messenger.send("main_menu_requested")
