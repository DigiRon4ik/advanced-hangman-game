import json
import os
from time import sleep
from random import choice

from colorama import init
from colorama import Fore, Back, Style

init(autoreset=True)
WORDS = {
    'ru': {
        'ПРОФЕССИЯ': ['СВАРЩИК', 'СПАСАТЕЛЬ', 'ПОВАР'],
        'ЖИВОТНОЕ': ['ЛИЧИНКА', 'МЕДУЗА', 'ОРАНГУТАН'],
        'Транспорт': ['ПОЕЗД', 'ВЕЛОСИПЕД', 'ЛОКОМОТИВ']
    },
    'en': {
        'PROFESSION': ['WELDER', 'RESCUER', 'COOK'],
        'ANIMAL': ['LARVA', 'MEDUSA', 'ORANGUTAN'],
        'TRANSPORT': ['TRAIN', 'BIKE', 'LOCOMOTIVE']
    }
}
SETTINGS = {
    'words': 'ru',
    'language': 'en',
    'difficulty': 'easy'
}
TRANSLATIONS = {}


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def close(msg=None) -> None:
    print(Fore.RED + 'EXIT...')
    sleep(0.5)
    __import__('sys').exit(msg)


def input_choice(expected: list, menu, input_msg='') -> int | str:
    choice = 0
    while True:
        try:
            choice = int(input(Style.BRIGHT + Fore.YELLOW + '  -->   ' +
                               Fore.GREEN + input_msg))
            if choice in expected:
                print()
                return choice
            else:
                menu(inp=False)
        except:
            menu(inp=False)


def print_log(msg: str, style=0, color=Fore.MAGENTA) -> None:
    if style == 0:
        style = Style.NORMAL
    else:
        style = Style.BRIGHT if style == 1 else Style.DIM

    print(Style.BRIGHT + Fore.CYAN + ' >> (log) | ' +
          style + color + msg)


def print_txt(befor: str, after: str, style=0, color=Fore.BLUE) -> None:
    if style == 0:
        style = Style.NORMAL
    else:
        style = Style.BRIGHT if style == 1 else Style.DIM

    print(Style.BRIGHT + Fore.YELLOW + befor +
          style + color + after)


def print_intro() -> None:
    try:
        file = open('data/intro.txt', 'r', encoding='utf-8')
        for i, v in enumerate(file):
            if i == 8:
                sleep(1.5)
            print(v, end='')
        file.close()
    except FileNotFoundError:
        print_log('INTRO-file was not found!\n', 1, Fore.RED)
        close(Fore.RED + '(./data/intro.txt)')
    else:
        print('\n')
    sleep(1)


def init_json() -> None:
    global WORDS
    with open('data/words.json', 'a+', encoding='utf-8') as file:
        file.seek(0)
        try:
            WORDS = json.load(file)
            print_log('JSON-words was loaded...', -1)
        except json.decoder.JSONDecodeError:
            json.dump(WORDS, file, indent=4, ensure_ascii=False)
            print_log('JSON-words was dumped...', -1)
        finally:
            print_log('JSON-words initialization succeeded!\n', 1)
    sleep(1)


def init_settings() -> None:
    global SETTINGS
    with open('data/settings.cfg', 'a+', encoding='utf-8') as file:
        file.seek(0)
        stg = file.read()
        if len(stg) != 0:
            stg = stg.strip().replace('\n', '=').replace(' ', '').split('=')
            SETTINGS = {stg[i]: stg[i + 1] for i in range(0, len(stg), 2)}
            print_log('SETTINGS was loaded...', -1)
        else:
            file.write(f'words={SETTINGS["words"]}\n'
                       f'language={SETTINGS["language"]}\n'
                       f'difficulty={SETTINGS["difficulty"]}')
            print_log('SETTINGS was dumped...', -1)
    print_log('Initialization of SETTINGS was successful!\n', 1)
    sleep(1)


def init_translations(lang='en') -> None:
    global TRANSLATIONS
    try:
        file = open('data/translations.json', 'r', encoding='utf-8')
        try:
            TRANSLATIONS = json.load(file)[lang]
            print_log(f'JSON-translations was loaded... [{lang}]', -1)
        except json.decoder.JSONDecodeError:
            print_log('JSON-translations file is empty!\n', 1, Fore.RED)
            close(Fore.RED + '(./data/translations.json)')
        file.close()
    except FileNotFoundError:
        print_log('JSON-translations file was not found!\n', 1, Fore.RED)
        close(Fore.RED + '(./data/translations.json)')
    else:
        print_log('JSON-translations initialization succeeded!\n', 1)
    sleep(1)


def main_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('> (1) | ', f'{TRANSLATIONS["play"]}', 1)
    print_txt('> (2) | ', f'{TRANSLATIONS["settings"]}', 1)
    print_txt('> (3) | ', f'{TRANSLATIONS["exit"]}', 1)
    if inp:
        choice = input_choice((1, 2, 3), main_menu)
        match choice:
            case 1:
                # play()
                pass
            case 2:
                # settings()
                pass
            case 3:
                close()


def main() -> None:
    clear_screen()
    init_json()
    init_settings()
    init_translations()
    print_intro()
    main_menu(clear=False)


if __name__ == "__main__":
    main()
