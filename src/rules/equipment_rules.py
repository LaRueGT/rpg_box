"""Pure equipment validation and derived descending-AC calculations."""

from model.item import EquipmentSlot, ItemType
from rules import ability_rules
from rules.encumbrance_rules import carrying_capacity, total_encumbrance


class EquipmentError(ValueError):
    pass


ARMOR_CLASS = {"leather": 7, "chainmail": 5, "plate mail": 3}


def _slot(slot):
    try:
        return slot if isinstance(slot, EquipmentSlot) else EquipmentSlot(str(slot).upper())
    except ValueError as exc:
        raise EquipmentError(f"unknown equipment slot: {slot}") from exc


def _equipped(character, slot):
    return character.inventory.equipped.get(slot)


def equip_item(character, item, slot):
    """Equip *item* in *slot*, raising EquipmentError when rules reject it."""
    slot = _slot(slot)
    if item not in character.inventory.items:
        raise EquipmentError("item must be in the character's inventory")
    if item.item_type == ItemType.WEAPON and slot != EquipmentSlot.MAIN_HAND:
        raise EquipmentError("weapons occupy the main hand")
    if item.item_type == ItemType.SHIELD and slot != EquipmentSlot.OFF_HAND:
        raise EquipmentError("shields occupy the off hand")
    if item.item_type == ItemType.ARMOR and slot != EquipmentSlot.BODY_ARMOR:
        raise EquipmentError("armor occupies the body armor slot")
    if item.item_type == ItemType.RING and slot not in (EquipmentSlot.RING_1, EquipmentSlot.RING_2):
        raise EquipmentError("rings occupy ring slots")
    if item.item_type not in (ItemType.WEAPON, ItemType.SHIELD, ItemType.ARMOR, ItemType.RING):
        raise EquipmentError("this item cannot be equipped")
    main = _equipped(character, EquipmentSlot.MAIN_HAND)
    off = _equipped(character, EquipmentSlot.OFF_HAND)
    if slot == EquipmentSlot.OFF_HAND and main and main.two_handed:
        raise EquipmentError("a two-handed weapon occupies both hands")
    if slot == EquipmentSlot.MAIN_HAND and item.two_handed and off:
        raise EquipmentError("two-handed weapons require an empty off hand")
    character.inventory.equipped[slot] = item
    return item


def unequip_item(character, slot):
    slot = _slot(slot)
    item = character.inventory.equipped[slot]
    character.inventory.equipped[slot] = None
    return item


def armor_class(character) -> int:
    armor = _equipped(character, EquipmentSlot.BODY_ARMOR)
    if armor is None:
        base = 9
    else:
        base = ARMOR_CLASS.get(armor.name.strip().lower(), armor.stat_modifiers.get("BASE_AC", 9))
    try:
        dexterity_adjustment = ability_rules.dexterity_ac_modifier(character.dexterity)
    except (TypeError, ValueError):
        dexterity_adjustment = 0
    ac = base - dexterity_adjustment
    shield = _equipped(character, EquipmentSlot.OFF_HAND)
    if shield and shield.item_type == ItemType.SHIELD:
        ac -= 1
    for item in character.inventory.equipped.values():
        if item:
            ac += item.stat_modifiers.get("AC", 0)
    return ac


def validate_encumbrance(character):
    weight = total_encumbrance(character.inventory)
    limit = carrying_capacity(character.strength)
    if weight > limit:
        raise EquipmentError(f"carrying {weight} coins exceeds the {limit}-coin capacity")
    return weight, limit


def transfer_item(source, target, item, container=None):
    if item not in source.inventory.items:
        raise EquipmentError("item is not in the source inventory")
    source.inventory.remove(item)
    try:
        target.inventory.add(item, container=container)
        validate_encumbrance(target)
    except Exception:
        source.inventory.add(item)
        raise


def drop_item(character, item):
    character.inventory.remove(item)
    return item
