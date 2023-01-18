from dataclasses import dataclass, field
import pandas as pd
import math

# Standardize how we handle attributes (vigor, mind, etc.)
StatBlock = dict[str: int]


# Standardize a rounding function
def round_down(n: float, dec: int = 0):
    if dec == 0:
        return math.floor(n)
    factor = 10 ** dec
    return math.floor(n * factor)/factor


# Defining a dataclass to handle our starting class attributes
@dataclass
class Origin:
    _name: str
    stat_block: StatBlock

    def __repr__(self) -> str:
        return f'{self._name}'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, _n: str) -> None:
        self._name = _n

    # Define our level property
    @property
    def level(self) -> int:
        return sum(self.stat_block.values()) - 79


# Initialize the object to hold each of the Origin classes we make
origins_dict = {}

# Create and format a dataframe from the origins.csv file
origins_df = pd.read_csv('origins.csv')
origins_df['Name'] = origins_df['Name'].astype('string')
origins_df.set_index('Name', inplace=True)

# Iterate through the dataframe and generate an Origin class from each row
for index, series in origins_df.iterrows():
    origins_dict[index] = Origin(str(index), series.to_dict())


# Define the Tarnished dataclass to handle instanced characters
@dataclass
class Tarnished:
    _name: str
    origin: Origin
    bonus_stat_block: StatBlock = field(init=False)

    # Generate our empty stat block of bonus stats
    def __post_init__(self) -> None:
        self.bonus_stat_block = {stat: 0 for stat in self.origin.stat_block}

    # Define our Name property
    @property
    def name(self) -> str:
        return self._name

    # Define our level property
    @property
    def level(self) -> int:
        return sum(self.bonus_stat_block.values()) + self.origin.level

    # Define our Runes Needed property
    def runes_needed(self, lvl: int = 0) -> int:
        if lvl == 0:
            lvl = self.level
        _x = max([((lvl + 81) - 92) * 0.02, 0])
        return 0 if lvl == 713 else math.floor(((_x + 0.1) * ((lvl + 81)**2)) + 1)

    # Define our Total Runes property
    def total_runes(self, lvl: int = 0) -> int:
        if lvl == 0:
            lvl = self.level
        if lvl == 1:
            return 0
        else:
            return self.runes_needed(lvl=lvl) + self.total_runes(lvl=lvl - 1)

    # Define setting a stat within possible parameters
    def set_stat(self, stat: str, val: int) -> None:
        if val <= 0:
            new_val = 0
        elif self.origin.stat_block[stat] + val >= 99:
            new_val = 99 - self.origin.stat_block[stat]
        else:
            new_val = val
        self.bonus_stat_block[stat] = new_val

    # Define Attribute properties for ease of use
    @property
    def vigor(self) -> int:
        return self.origin.stat_block['Vigor'] + self.bonus_stat_block['Vigor']

    @property
    def mind(self) -> int:
        return self.origin.stat_block['Mind'] + self.bonus_stat_block['Mind']

    @property
    def endurance(self) -> int:
        return self.origin.stat_block['Endurance'] + self.bonus_stat_block['Endurance']

    @property
    def strength(self) -> int:
        return self.origin.stat_block['Strength'] + self.bonus_stat_block['Strength']

    @property
    def dexterity(self) -> int:
        return self.origin.stat_block['Dexterity'] + self.bonus_stat_block['Dexterity']

    @property
    def intelligence(self) -> int:
        return self.origin.stat_block['Intelligence'] + self.bonus_stat_block['Intelligence']

    @property
    def faith(self) -> int:
        return self.origin.stat_block['Faith'] + self.bonus_stat_block['Faith']

    @property
    def arcane(self) -> int:
        return self.origin.stat_block['Arcane'] + self.bonus_stat_block['Arcane']

    # Now the real fun part... Defining derived stats as properties (HP, FP, Defense, Discovery, etc.)
    @property
    def hit_points(self) -> int:
        if self.vigor < 26:
            return round_down(300 + 500 * (((self.vigor - 1) / 24) ** 1.5))
        elif self.vigor < 41:
            return round_down(800 + 650 * (((self.vigor - 25) / 15) ** 1.1))
        elif self.vigor < 61:
            return round_down(1450 + 450 * (1 - (1 - ((self.vigor - 40) / 20)) ** 1.2))
        else:
            return round_down(1900 + 200 * (1 - (1 - ((self.vigor - 60) / 39)) ** 1.2))

    @property
    def focus_points(self) -> int:
        if self.mind < 16:
            return round_down(50 + 45 * ((self.mind - 1) / 14))
        elif self.mind < 36:
            return round_down(95 + 105 * ((self.mind - 15) / 20))
        elif self.mind < 61:
            return round_down(200 + 150 * (1 - (1 - ((self.mind - 35) / 25)) ** 1.2))
        else:
            return round_down(350 + 100 * ((self.mind - 60) / 39))

    @property
    def stamina(self) -> int:
        if self.endurance < 16:
            return round_down(80 + 25 * ((self.endurance - 1) / 14))
        elif self.endurance < 36:
            return round_down(105 + 25 * ((self.endurance - 15) / 15))
        elif self.endurance < 61:
            return round_down(130 + 25 * ((self.endurance - 30) / 20))
        else:
            return round_down(155 + 15 * ((self.endurance - 50) / 49))

    @property
    def immunity(self) -> int:
        if self.level < 72:
            lvl_prt = 75 + 30 * ((self.level + 78) / 149)
        elif self.level < 112:
            lvl_prt = 105 + 40 * ((self.level - 71) / 40)
        elif self.level < 162:
            lvl_prt = 145 + 15 * ((self.level - 91) / 50)
        else:
            lvl_prt = 160 + 20 * ((self.level - 161) / 552)
        if self.vigor < 31:
            vig_prt = 0
        elif self.vigor < 41:
            vig_prt = 30 * ((self.vigor - 30) / 10)
        elif self.vigor < 61:
            vig_prt = 30 + 10 * ((self.vigor - 40) / 20)
        else:
            vig_prt = 40 + 10 * ((self.vigor - 60) / 39)
        return round_down(lvl_prt + vig_prt)

    @property
    def focus(self) -> int:
        if self.level < 72:
            lvl_prt = 75 + 30 * ((self.level + 78) / 149)
        elif self.level < 112:
            lvl_prt = 105 + 40 * ((self.level - 71) / 40)
        elif self.level < 162:
            lvl_prt = 145 + 15 * ((self.level - 91) / 50)
        else:
            lvl_prt = 160 + 20 * ((self.level - 161) / 552)
        if self.mind < 31:
            mnd_prt = 0
        elif self.mind < 41:
            mnd_prt = 30 * ((self.mind - 30) / 10)
        elif self.mind < 61:
            mnd_prt = 30 + 10 * ((self.mind - 40) / 20)
        else:
            mnd_prt = 40 + 10 * ((self.mind - 60) / 39)
        return round_down(lvl_prt + mnd_prt)

    @property
    def robustness(self) -> int:
        if self.level < 72:
            lvl_prt = 75 + 30 * ((self.level + 78) / 149)
        elif self.level < 112:
            lvl_prt = 105 + 40 * ((self.level - 71) / 40)
        elif self.level < 162:
            lvl_prt = 145 + 15 * ((self.level - 91) / 50)
        else:
            lvl_prt = 160 + 20 * ((self.level - 161) / 552)
        if self.endurance < 31:
            end_prt = 0
        elif self.endurance < 41:
            end_prt = 30 * ((self.endurance - 30) / 10)
        elif self.endurance < 61:
            end_prt = 30 + 10 * ((self.endurance - 40) / 20)
        else:
            end_prt = 40 + 10 * ((self.endurance - 60) / 39)
        return round_down(lvl_prt + end_prt)

    @property
    def equip_load(self) -> float:
        if self.endurance < 26:
            return round_down(45 + 27 * ((self.endurance - 8) / 17), 1)
        elif self.endurance < 61:
            return round_down(72 + 48 * (((self.endurance - 25) / 35) ** 1.1), 1)
        else:
            return round_down(120 + 40 * ((self.endurance - 60) / 39), 1)

    @property
    def discovery(self) -> int:
        return 100 + self.arcane

    @property
    def vitality(self) -> int:
        if self.level < 72:
            lvl_prt = 75 + 30 * ((self.level + 78) / 149)
        elif self.level < 112:
            lvl_prt = 105 + 40 * ((self.level - 71) / 40)
        elif self.level < 162:
            lvl_prt = 145 + 15 * ((self.level - 91) / 50)
        else:
            lvl_prt = 160 + 20 * ((self.level - 161) / 552)
        if self.arcane < 16:
            arc_prt = self.arcane
        elif self.arcane < 41:
            arc_prt = 15 + 15 * ((self.arcane - 15) / 25)
        elif self.arcane < 61:
            arc_prt = 30 + 10 * ((self.arcane - 40) / 20)
        else:
            arc_prt = 40 + 10 * ((self.arcane - 60) / 39)
        return round_down(lvl_prt + arc_prt)

    @property
    def physical_defense(self) -> int:
        if self.level < 72:
            lvl_prt = 40 + 60 * ((self.level + 78) / 149)
        elif self.level < 91:
            lvl_prt = 100 + 20 * ((self.level - 71) / 20)
        elif self.level < 162:
            lvl_prt = 120 + 15 * ((self.level - 91) / 70)
        else:
            lvl_prt = 135 + 20 * ((self.level - 161) / 552)
        if self.strength < 30:
            str_prt = 10 * (self.strength / 30)
        elif self.strength < 41:
            str_prt = 10 + 5 * ((self.strength - 30) / 10)
        elif self.strength < 61:
            str_prt = 15 + 15 * ((self.strength - 40) / 20)
        else:
            str_prt = 30 + 10 * ((self.strength - 60) / 39)
        return round_down(lvl_prt + str_prt)

    @property
    def magic_defense(self) -> int:
        if self.level < 72:
            lvl_prt = 40 + 60 * ((self.level + 78) / 149)
        elif self.level < 91:
            lvl_prt = 100 + 20 * ((self.level - 71) / 20)
        elif self.level < 162:
            lvl_prt = 120 + 15 * ((self.level - 91) / 70)
        else:
            lvl_prt = 135 + 20 * ((self.level - 161) / 552)
        if self.intelligence < 21:
            int_prt = 40 * (self.intelligence / 20)
        elif self.intelligence < 36:
            int_prt = 40 + 10 * ((self.intelligence - 20) / 15)
        elif self.intelligence < 61:
            int_prt = 50 + 10 * ((self.intelligence - 35) / 25)
        else:
            int_prt = 60 + 10 * ((self.intelligence - 60) / 39)
        return round_down(lvl_prt + int_prt)

    @property
    def lightning_defense(self) -> int:
        if self.level < 72:
            lvl_prt = 40 + 60 * ((self.level + 78) / 149)
        elif self.level < 91:
            lvl_prt = 100 + 20 * ((self.level - 71) / 20)
        elif self.level < 162:
            lvl_prt = 120 + 15 * ((self.level - 91) / 70)
        else:
            lvl_prt = 135 + 20 * ((self.level - 161) / 552)
        return round_down(lvl_prt)

    @property
    def fire_defense(self) -> int:
        if self.level < 72:
            lvl_prt = 40 + 60 * ((self.level + 78) / 149)
        elif self.level < 91:
            lvl_prt = 100 + 20 * ((self.level - 71) / 20)
        elif self.level < 162:
            lvl_prt = 120 + 15 * ((self.level - 91) / 70)
        else:
            lvl_prt = 135 + 20 * ((self.level - 161) / 552)
        if self.strength < 30:
            str_prt = 20 * (self.strength / 30)
        elif self.strength < 41:
            str_prt = 20 + 20 * ((self.strength - 30) / 10)
        elif self.strength < 61:
            str_prt = 40 + 20 * ((self.strength - 40) / 20)
        else:
            str_prt = 60 + 10 * ((self.strength - 60) / 39)
        return round_down(lvl_prt + str_prt)

    @property
    def holy_defense(self) -> int:
        if self.level < 72:
            lvl_prt = 40 + 60 * ((self.level + 78) / 149)
        elif self.level < 91:
            lvl_prt = 100 + 20 * ((self.level - 71) / 20)
        elif self.level < 162:
            lvl_prt = 120 + 15 * ((self.level - 111) / 70)
        else:
            lvl_prt = 135 + 20 * ((self.level - 240) / 552)
        if self.arcane < 20:
            arc_prt = 40 * (self.arcane / 20)
        elif self.arcane < 36:
            arc_prt = 40 + 10 * ((self.arcane - 20) / 15)
        elif self.arcane < 61:
            arc_prt = 50 + 10 * ((self.arcane - 35) / 25)
        else:
            arc_prt = 60 + 10 * ((self.arcane - 60) / 39)
        return round_down(lvl_prt + arc_prt)
