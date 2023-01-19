from src.char_data import Tarnished, origins_dict
import re
import os


def display_char(char) -> None:
    print()
    print(f'Name: {char.name}')
    print(f'Lvl. {char.level:03} {char.origin.name}')
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
    mod_commands = ['+', '-', '=']
    command_pattern = '(?P<stat>\w+)\s(?P<mod>.)\s(?P<val>\d+)'
    test_tarnished = Tarnished(_name='Let Me Solo Her', origin=origins_dict['Samurai'])
    running = True
    while running:
        os.system('clear')
        display_char(test_tarnished)
        response = input('Stat Adjust: ')
        if response.lower() in ['q', 'quit']:
            running = False
        elif response.lower() in ['h', 'help']:
            print('Ex. "str + 5"')
            print()
        else:
            command = re.fullmatch(command_pattern, response.lower())
            if not command:
                os.system('clear')
                print('Invalid Syntax!')
                print('Enter "h" or "help" for command syntax')
                print()
            elif command.group('stat') not in stat_commands:
                os.system('clear')
                print('Invalid Stat!')
                print('Valid Stat Ex. "str" or "strength"')
                print()
            elif command.group('mod') not in mod_commands:
                os.system('clear')
                print('Invalid Mod!')
                print('Valid Mods are "+", "=", and "-"')
                print()
            else:
                os.system('clear')
                stat = stat_commands[command.group('stat')]
                val = int(command.group('val'))
                if command.group('mod') == '+':
                    test_tarnished.set_stat(stat, val)
                elif command.group('mod') == '=':
                    test_tarnished.set_stat(stat, val - test_tarnished.origin.stat_block[stat])
                else:
                    test_tarnished.set_stat(stat, -val)
