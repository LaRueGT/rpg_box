"""Item data used by inventory and equipment rules.

The model deliberately contains no Panda3D or UI concerns.  Weights use the
classic Gold Box convention: one weight unit is one coin.
"""

from dataclasses import dataclass, field
from enum import StrEnum


class ItemType(StrEnum):
    WEAPON = "WEAPON"
    ARMOR = "ARMOR"
    SHIELD = "SHIELD"
    RING = "RING"
    MISC = "MISC"


class EquipmentSlot(StrEnum):
    MAIN_HAND = "MAIN_HAND"
    OFF_HAND = "OFF_HAND"
    BODY_ARMOR = "BODY_ARMOR"
    RING_1 = "RING_1"
    RING_2 = "RING_2"


@dataclass(eq=False)
class Item:
    name: str
    weight: int | float = 80
    gold_value: int | float = 0
    item_type: ItemType = ItemType.MISC
    stat_modifiers: dict[str, int] = field(default_factory=dict)
    quantity: int = 1
    two_handed: bool = False
    container_capacity: int | float | None = None
    container_size: str | None = None  # "small" may be belted; "large" needs hands

    def __post_init__(self):
        if isinstance(self.item_type, str):
            self.item_type = ItemType(self.item_type.upper())
        if self.quantity < 1:
            raise ValueError("item quantity must be positive")
        if self.weight < 0:
            raise ValueError("item weight cannot be negative")

    @property
    def is_container(self) -> bool:
        return self.container_capacity is not None

    @property
    def is_small_container(self) -> bool:
        return self.container_size == "small"

    @property
    def is_large_container(self) -> bool:
        return self.container_size == "large"

    @property
    def total_weight(self):
        return self.weight * self.quantity
