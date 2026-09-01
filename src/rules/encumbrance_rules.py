"""Encumbrance and movement rules.

Weights are expressed in coins, matching the equipment tables in ``data``.
The image tables are kept as reference material, so the small lookup tables
below are the executable version of the weights needed by the game.
"""

from dataclasses import dataclass
from numbers import Integral, Real
from collections.abc import Iterable, Mapping
import re

from model.inventory import Inventory


MISCELLANEOUS_ITEM_WEIGHT = 80

# Equipment weights from armor_table.png, weapons_table.png, and
# treasure_table.png.  Keys are normalized before lookup.
ITEM_WEIGHTS = {
    "leather": 200,
    "chainmail": 400,
    "plate mail": 500,
    "shield": 100,
    "battle axe": 50,
    "club": 50,
    "crossbow": 50,
    "dagger": 10,
    "hand axe": 30,
    "javelin": 20,
    "lance": 120,
    "long bow": 30,
    "mace": 30,
    "pole arm": 150,
    "short bow": 30,
    "short sword": 30,
    "silver dagger": 10,
    "sling": 20,
    "spear": 30,
    "staff": 40,
    "sword": 60,
    "two-handed sword": 150,
    "war hammer": 30,
    "coin": 1,
    "coin (any type)": 1,
    "gem": 1,
    "jewellery": 10,
    "jewelry": 10,
    "potion": 10,
    "rod": 20,
    "scroll": 1,
    "wand": 10,
}


@dataclass(frozen=True)
class InventoryItem:
    """An item in a character's inventory.

    ``weight`` is optional and is useful for adding a future table entry.
    Items without a table entry use the miscellaneous weight of 80 coins.
    """

    name: str
    quantity: int = 1
    weight: Real | None = None


def _normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower().replace("’", "'")).replace(
        "jewellery (1 piece)", "jewellery"
    )


def item_weight(item: InventoryItem | str | Mapping[str, object] | object) -> Real:
    """Return the weight in coins of one item (not its quantity)."""
    if isinstance(item, InventoryItem):
        if item.weight is not None:
            return item.weight
        name = item.name
    elif isinstance(item, str):
        name = item
    elif isinstance(item, Mapping):
        name = item.get("name", "")
        if "weight" in item and item["weight"] is not None:
            return item["weight"]
    else:
        name = getattr(item, "name", "")
        explicit_weight = getattr(item, "weight", None)
        if explicit_weight is not None:
            return explicit_weight

    if not isinstance(name, str):
        raise TypeError("inventory item name must be a string")
    return ITEM_WEIGHTS.get(_normalize_name(name), MISCELLANEOUS_ITEM_WEIGHT)


def _is_miscellaneous(item: InventoryItem | str | Mapping[str, object] | object) -> bool:
    """Whether an item is covered by the single miscellaneous-item allowance."""
    if isinstance(item, InventoryItem):
        return item.weight is None and _normalize_name(item.name) not in ITEM_WEIGHTS
    if isinstance(item, str):
        return _normalize_name(item) not in ITEM_WEIGHTS
    if isinstance(item, Mapping):
        if item.get("weight") is not None:
            return False
        name = item.get("name", "")
    else:
        if getattr(item, "weight", None) is not None:
            return False
        name = getattr(item, "name", "")
    return not isinstance(name, str) or _normalize_name(name) not in ITEM_WEIGHTS


def _quantity(item: InventoryItem | str | Mapping[str, object] | object) -> int:
    quantity = item.quantity if isinstance(item, InventoryItem) else (
        item.get("quantity", 1) if isinstance(item, Mapping) else getattr(item, "quantity", 1)
    )
    if isinstance(quantity, bool) or not isinstance(quantity, Integral) or quantity < 1:
        raise ValueError("inventory item quantity must be a positive integer")
    return quantity


def total_encumbrance(inventory: Iterable[InventoryItem | str | Mapping[str, object] | object]) -> Real:
    """Return total carried weight, grouping all miscellaneous items as 80 coins.

    This deliberately treats miscellaneous weight as a single shorthand
    allowance, regardless of how many miscellaneous items are carried.
    """
    if isinstance(inventory, Inventory):
        # Every item is listed once in Inventory, including equipped items;
        # container contents therefore count naturally without double-counting.
        return _inventory_weight(inventory)
    total = 0
    has_miscellaneous_items = False
    for item in inventory:
        if _is_miscellaneous(item):
            has_miscellaneous_items = True
        else:
            total += item_weight(item) * _quantity(item)
    return total + (MISCELLANEOUS_ITEM_WEIGHT if has_miscellaneous_items else 0)


def _inventory_weight(inventory: Inventory) -> Real:
    total = 0
    has_legacy_misc = False
    for item in inventory.items:
        if _is_miscellaneous(item):
            has_legacy_misc = True
        else:
            total += item_weight(item) * _quantity(item)
    # New Item records have an explicit weight. Legacy InventoryItems preserve
    # the old shared miscellaneous allowance for backwards-compatible saves.
    return total + (MISCELLANEOUS_ITEM_WEIGHT if has_legacy_misc else 0)


def carrying_capacity(strength: int) -> int:
    """Maximum carried coins using the B/X 10 coins per point of STR rule."""
    if not isinstance(strength, Integral) or strength < 0:
        raise ValueError("strength must be a non-negative integer")
    return min(1600, strength * 10) if strength else 1600


def encumbrance_state(inventory, strength: int) -> tuple[Real, int, int]:
    weight = total_encumbrance(inventory)
    return weight, carrying_capacity(strength), movement_rate(weight)


def movement_rate(weight: Real) -> int:
    """Return the normal movement rate for a carried weight in coins.

    The detailed table uses inclusive upper bounds.  More than 1,600 coins
    leaves a character unable to move under these rules.
    """
    if isinstance(weight, bool) or not isinstance(weight, Real):
        raise TypeError("encumbrance must be a number")
    if weight < 0:
        raise ValueError("encumbrance cannot be negative")
    if weight <= 400:
        return 120
    if weight <= 600:
        return 90
    if weight <= 800:
        return 60
    if weight <= 1600:
        return 30
    return 0


def movement_rate_for_inventory(inventory: Iterable[InventoryItem | str | Mapping[str, object] | object]) -> int:
    """Return movement rate after applying the inventory's encumbrance."""
    return movement_rate(total_encumbrance(inventory))


# Short aliases for callers that prefer the terminology used by the table.
encumbrance = total_encumbrance
movement = movement_rate_for_inventory
