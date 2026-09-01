import pytest

from model.character import Character
from rules.encumbrance_rules import (
    InventoryItem,
    item_weight,
    movement_rate,
    movement_rate_for_inventory,
    total_encumbrance,
)


@pytest.mark.parametrize(
    ("weight", "expected"),
    [(400, 120), (401, 90), (600, 90), (601, 60), (800, 60), (801, 30), (1600, 30), (1601, 0)],
)
def test_movement_rate_uses_inclusive_encumbrance_bands(weight, expected):
    assert movement_rate(weight) == expected


def test_table_items_and_miscellaneous_items_have_expected_weights():
    inventory = [InventoryItem("Plate mail"), InventoryItem("Sword"), "bedroll"]
    assert total_encumbrance(inventory) == 500 + 60 + 80


def test_quantity_and_unknown_items_are_counted():
    assert item_weight("gem") == 1
    assert total_encumbrance([InventoryItem("torch", quantity=3)]) == 80
    assert movement_rate_for_inventory([InventoryItem("Plate mail"), "bedroll"]) == 90


def test_miscellaneous_items_share_one_80_coin_allowance():
    assert total_encumbrance(["chain", "lock", "bell"]) == 80
    assert total_encumbrance(["sword", "chain", "lock", "bell"]) == 140
    assert total_encumbrance(["sword"]) == 60


def test_character_has_minimal_inventory_and_encumbrance_properties():
    character = Character()
    character.add_item("chainmail")
    character.add_item("rations", quantity=2)
    assert character.encumbrance == 480
    assert character.movement_rate == 90


def test_invalid_encumbrance_is_rejected():
    with pytest.raises(ValueError):
        movement_rate(-1)
