class Character:
    def __init__(self):
        self.strength = 0
        self.intelligence = 0
        self.wisdom = 0
        self.dexterity = 0
        self.constitution = 0
        self.charisma = 0
        self.char_race = None
        self.gender = None
        self.char_classes = []
        self.exp_factor = []
        self.level = [1]
        self.exp_amount = []
        self.char_alignment = None
        self.thaco = 19
        self.attack_values = {}
        # Targets are populated by leveling_rules once classes are selected.
        # A lower target is better; None means no class has been assigned yet.
        self.saving_throws = {
            "death_poison": None,
            "wands": None,
            "paralysis_petrify": None,
            "breath": None,
            "spells_rods_staves": None,
        }
        self.max_hp = 0
        self.hp_fraction = 0
        self.name = ""
        from model.inventory import Inventory

        self.inventory = Inventory(owner=self)

    def add_item(self, item, quantity=1, weight=None):
        """Add a small inventory entry; rules resolve its weight later."""
        from model.item import Item

        if isinstance(item, Item):
            if quantity != 1:
                item.quantity = quantity
            self.inventory.add(item)
            return item
        from rules.encumbrance_rules import InventoryItem

        self.inventory.append(InventoryItem(item, quantity, weight))

    @property
    def encumbrance(self):
        from rules.encumbrance_rules import total_encumbrance

        return total_encumbrance(self.inventory)

    @property
    def movement_rate(self):
        from rules.encumbrance_rules import movement_rate

        return movement_rate(self.encumbrance)

    @property
    def armor_class(self):
        from rules.equipment_rules import armor_class
        return armor_class(self)

    @property
    def carrying_capacity(self):
        from rules.encumbrance_rules import carrying_capacity
        return carrying_capacity(self.strength)
