"""A character's physical inventory and equipment slots."""

from collections.abc import Iterator

from model.item import EquipmentSlot, Item


class Inventory:
    def __init__(self, items=None, owner=None):
        self.owner = owner
        self.items: list[Item] = []
        self.equipped: dict[EquipmentSlot, Item | None] = {
            slot: None for slot in EquipmentSlot
        }
        self.container_contents: dict[Item, list[Item]] = {}
        self.item_hands: set[Item] = set()
        if items:
            for item in items:
                self.add(item)

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def append(self, item):
        """List-compatible alias retained for old save/setup code."""
        self.add(item)

    def add(self, item, container=None, in_hands=False):
        if isinstance(item, str):
            item = Item(str(item))
        if item in self.items:
            raise ValueError("the same item instance is already in the inventory")
        # A large container cannot be belted or left floating in the pack: it
        # occupies both hands. Legacy InventoryItems remain permissive for old
        # character data and tests.
        if isinstance(item, Item) and item.is_large_container and not in_hands:
            raise ValueError("large containers must be carried in both hands")
        if container is not None:
            self._validate_container(container, item)
            self.container_contents.setdefault(container, []).append(item)
        elif in_hands:
            self.item_hands.add(item)
        self.items.append(item)
        if self.owner is not None:
            from rules.encumbrance_rules import carrying_capacity, total_encumbrance
            if total_encumbrance(self) > carrying_capacity(self.owner.strength):
                self.remove(item)
                raise ValueError("adding this item exceeds the character's carrying capacity")
        return item

    def remove(self, item):
        if item not in self.items:
            raise ValueError("item is not in this inventory")
        for slot, equipped in list(self.equipped.items()):
            if equipped is item:
                self.equipped[slot] = None
        for contents in self.container_contents.values():
            if item in contents:
                contents.remove(item)
        self.container_contents.pop(item, None)
        self.item_hands.discard(item)
        self.items.remove(item)
        return item

    def _validate_container(self, container, item):
        if container not in self.items or not getattr(container, "is_container", False):
            raise ValueError("items must be placed in a container the character owns")
        if container is item:
            raise ValueError("a container cannot contain itself")
        item_weight = getattr(item, "total_weight", 0)
        if self.container_weight(container) + item_weight > container.container_capacity:
            raise ValueError(f"{container.name} does not have enough capacity")

    def move_to_container(self, item, container):
        if item not in self.items:
            raise ValueError("item is not in this inventory")
        for contents in self.container_contents.values():
            if item in contents:
                contents.remove(item)
        self._validate_container(container, item)
        self.container_contents.setdefault(container, []).append(item)
        self.item_hands.discard(item)

    def container_weight(self, container):
        return sum(getattr(item, "total_weight", 0) for item in self.container_contents.get(container, ()))

    def contents_of(self, container):
        return tuple(self.container_contents.get(container, ()))

    def location_of(self, item):
        for slot, equipped in self.equipped.items():
            if equipped is item:
                return slot
        for container, contents in self.container_contents.items():
            if item in contents:
                return container
        if item in self.item_hands:
            return "HANDS"
        return "UNASSIGNED"

    @property
    def containers(self):
        return tuple(item for item in self.items if getattr(item, "is_container", False))
