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
