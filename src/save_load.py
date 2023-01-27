import pandas as pd
import src.char_data as char_data
from collections import OrderedDict


# A template for a null save file
null_save = {
        'Name': None,
        'Origin': 'Null',
        'Vigor': None,
        'Mind': None,
        'Endurance': None,
        'Strength': None,
        'Dexterity': None,
        'Intelligence': None,
        'Faith': None,
        'Arcane': None
    }


# Creates a save ID number based on the highest ID in the current save file
def gen_save_id() -> str:
    with open('src/saves.csv', 'r') as save_file:
        saves_df = pd.read_csv(save_file)
        new_id = max(list(saves_df.index.values)) + 1
    return f'{new_id:04}'


# Loads a character from the save file with a given save slot
def load_char(save_slot: int) -> [char_data.Tarnished, bool]:
    success = True
    with open('src/saves.csv', 'r') as save_file:
        saves_dict = pd.read_csv(save_file).to_dict('index')
    if save_slot == 0 or save_slot not in saves_dict or saves_dict[save_slot]['Origin'] == 'Null':
        save_slot = 0
        success = False
    tarnished_name = saves_dict[save_slot]['Name']
    tarnished_origin = saves_dict[save_slot]['Origin']
    loaded_tarnished = char_data.Tarnished(_name=tarnished_name, origin=char_data.origins_dict[tarnished_origin])
    for stat in loaded_tarnished.bonus_stat_block:
        loaded_tarnished.set_stat(stat, saves_dict[save_slot][stat])
    return loaded_tarnished, success


# Saves a character to the save file with a given save slot
def save_char(save_slot: int, char: char_data.Tarnished) -> None:
    field_names = ['Name', 'Origin', 'Vigor', 'Mind', 'Endurance',
                   'Strength', 'Dexterity', 'Intelligence', 'Faith', 'Arcane']
    char_save_dict = {
        'Name': char.name,
        'Origin': char.origin,
        'Vigor': char.bonus_stat_block['Vigor'],
        'Mind': char.bonus_stat_block['Mind'],
        'Endurance': char.bonus_stat_block['Endurance'],
        'Strength': char.bonus_stat_block['Strength'],
        'Dexterity': char.bonus_stat_block['Dexterity'],
        'Intelligence': char.bonus_stat_block['Intelligence'],
        'Faith': char.bonus_stat_block['Faith'],
        'Arcane': char.bonus_stat_block['Arcane']
    }
    with open('src/saves.csv', 'r') as save_file:
        saves_dict = pd.read_csv(save_file).to_dict('index')
    saves_dict[save_slot] = char_save_dict
    for i in range(0, max(saves_dict.keys())):
        if i not in saves_dict:
            saves_dict[i] = null_save
    for i in range(0, max(saves_dict.keys())+1):
        saves_dict = OrderedDict(saves_dict)
        saves_dict.move_to_end(i)
    saves_df = pd.DataFrame.from_dict(saves_dict, orient='index', columns=field_names)
    with open('src/saves.csv', 'w') as save_file:
        saves_df.to_csv(save_file, columns=field_names, index_label='ID')


# Define a way to view the saved characters
def list_save_slots() -> list:
    with open('src/saves.csv', 'r') as save_file:
        saves_dict = pd.read_csv(save_file).to_dict('index')
    return [(saves_dict[slot]['ID'], saves_dict[slot]['Name'], saves_dict[slot]['Origin'])
            for slot in saves_dict if slot != 0]
