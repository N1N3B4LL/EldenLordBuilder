from src.save_load import load_char, save_char, list_save_slots
from src.char_data import origins_dict
import re
import os


def display_char(char) -> None:
    print()
    print(f'Name: {char.name}')
    print(f'Lvl. {char.level:03} {char.origin.name}')
    print(f'Total Runes: {char.total_runes} | Runes Needed: {char.runes_needed()}')
    print('*-ATTRIBUTES-*')
    print(f'VIG: {char.vigor:02} | MND: {char.mind:02} | END: {char.endurance:02} | STR: {char.strength:02}')
    print(f'DEX: {char.dexterity:02} | INT: {char.intelligence:02} | FTH: {char.faith:02} | ARC: {char.arcane:02}')
    print('*-CORE STATS-*')
    print(f'HP: {char.hit_points:04} | FP: {char.focus_points:03} | Stamina: {char.stamina:03}')
    print(f'Max Equip Load: {char.equip_load:05} | Discovery: {char.discovery:03}')
    print('*-BODY-*')
    print(f'Imm: {char.immunity:03} | Rob: {char.robustness:03} | Foc: {char.focus:03} | Vit: {char.vitality:03}')
    print('*-DEFENSES-*')
    print(f'Physical: {char.physical_defense:03} | Magic: {char.magic_defense:03} | Fire: {char.fire_defense:03} | Lightning: {char.lightning_defense:03} | Holy: {char.holy_defense:03}')
    print()


if __name__ == '__main__':
    stat_commands = {
        'vig': 'Vigor', 'vigor': 'Vigor', 'mnd': 'Mind', 'mind': 'Mind', 'end': 'Endurance', 'endurance': 'Endurance',
        'str': 'Strength', 'strength': 'Strength', 'dex': 'Dexterity', 'dexterity': 'Dexterity', 'int': 'Intelligence',
        'intelligence': 'Intelligence', 'fth': 'Faith', 'faith': 'Faith', 'arc': 'Arcane', 'Arcane': 'arcane'
    }
    mod_commands = ['=']
    stat_adjust_pattern = '(?P<stat>\w+)\s(?P<mod>.)\s(?P<val>\d+)'
    new_name_pattern = '(?P<command>name)\s(?P<new_name>.+)'
    new_origin_pattern = '(?P<command>origin)\s(?P<new_origin>.+)'
    save_load_pattern = '(?P<command>save|load)\s(?P<save_slot>\d+)'
    test_tarnished, _bool = load_char(0)
    running = True
    while running:
        display_char(test_tarnished)
        response = input('? ')
        if response.lower() in ['q', 'quit']:
            running = False
        elif re.fullmatch(stat_adjust_pattern, response.lower()):
            command = re.fullmatch(stat_adjust_pattern, response.lower())
            if command.group('stat') not in stat_commands:
                os.system('clear')
                os.system('clear')
                print('Invalid Stat!')
                print('Valid Stat Ex. "str" or "strength"')
                print()
            elif command.group('mod') not in mod_commands:
                os.system('clear')
                os.system('clear')
                print('Invalid Mod!')
                print('Valid Mods are: "="')
                print()
            else:
                os.system('clear')
                os.system('clear')
                stat = stat_commands[command.group('stat')]
                val = int(command.group('val'))
                test_tarnished.set_stat(stat, val - test_tarnished.origin.stat_block[stat])
        elif re.fullmatch(new_name_pattern, response.lower()):
            command = re.fullmatch(new_name_pattern, response)
            if len(command.group('new_name')) > 16:
                os.system('clear')
                os.system('clear')
                print('Invalid Name!')
                print('Names must be 16 characters or less')
                print()
            else:
                os.system('clear')
                os.system('clear')
                new_name = command.group('new_name')
                test_tarnished.set_name(new_name)
        elif re.fullmatch(new_origin_pattern, response.lower()):
            command = re.fullmatch(new_origin_pattern, response)
            if command.group('new_origin') not in [org for org in origins_dict]:
                os.system('clear')
                os.system('clear')
                print('Invalid Origin')
                print('Valid Origins are: ' + ', '.join([org for org in origins_dict]))
            else:
                os.system('clear')
                os.system('clear')
                new_origin = origins_dict[command.group('new_origin')]
                test_tarnished.set_origin(new_origin)
        elif re.fullmatch(save_load_pattern, response.lower()):
            command = re.fullmatch(save_load_pattern, response.lower())
            if int(command.group('save_slot')) < 1:
                os.system('clear')
                os.system('clear')
                print('Invalid slot ID!')
                print('Save Slot must be a positive integer')
            if command.group('command') == 'save':
                os.system('clear')
                os.system('clear')
                save_char(int(command.group('save_slot')), test_tarnished)
                print(f'{test_tarnished.name} saved successfully to slot {command.group("save_slot")}')
                print()
            else:
                os.system('clear')
                os.system('clear')
                test_tarnished, success_check = load_char(int(command.group('save_slot')))
                if success_check:
                    print(f'{test_tarnished.name} loaded successfully from slot {command.group("save_slot")}')
                else:
                    print('ERROR!')
                    print(f'No Tarnished found in slot: {command.group("save_slot")}')
                print()
        elif response.lower() == 'list':
            os.system('clear')
            os.system('clear')
            print(list_save_slots())
            print()
        else:
            os.system('clear')
            os.system('clear')
            print('ERROR! UNRECOGNIZED COMMAND!')
            print()
