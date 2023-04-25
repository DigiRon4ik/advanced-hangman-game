import json
import os
from time import sleep
from random import choice

from colorama import init
from colorama import Fore, Back, Style

from hangman_ascii import print_hangman

init(autoreset=True)
WORDS = {
    'ru': {
        'ПРОФЕССИЯ': ['СВАРЩИК', 'СПАСАТЕЛЬ', 'ПОВАР'],
        'ЖИВОТНОЕ': ['ЛИЧИНКА', 'МЕДУЗА', 'ОРАНГУТАН'],
        'ТРАНСПОРТ': ['ПОЕЗД', 'ВЕЛОСИПЕД', 'ЛОКОМОТИВ']
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


def input_choice(expected: tuple | int, menu=None, input_msg='') -> int | str:
    choice = 0
    while True:
        try:
            choice = int(input(Style.BRIGHT + Fore.YELLOW + '  -->   ' +
                               Fore.GREEN + input_msg))
            if isinstance(expected, int) and 1 <= choice <= expected:
                print()
                return choice
            if choice in expected:
                print()
                return choice
            else:
                raise
        except:
            if menu is not None:
                menu(inp=False)
            else:
                print_txt('', TRANSLATIONS["wrong_choice"], 1, Fore.RED)


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


def init_json(mode='a+') -> None:
    global WORDS
    with open('data/words.json', mode=mode, encoding='utf-8') as file:
        file.seek(0)
        try:
            WORDS = json.load(file)
            print_log('JSON-words was loaded...', -1)
        except:
            json.dump(WORDS, file, indent=4, ensure_ascii=False)
            print_log('JSON-words was dumped...', -1)
        finally:
            print_log('JSON-words initialization succeeded!\n', 1)
    sleep(1)


def init_settings(mode='a+') -> None:
    global SETTINGS
    with open('data/settings.cfg', mode=mode, encoding='utf-8') as file:
        file.seek(0)
        if mode == 'a+':
            stg = file.read()
        if mode == 'a+' and len(stg) != 0:
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
    print_txt('> (1) | ', TRANSLATIONS["play"], 1)
    print_txt('> (2) | ', TRANSLATIONS["settings"], 1)
    print_txt('> (3) | ', TRANSLATIONS["exit"], 1)
    if inp:
        choice = input_choice((1, 2, 3), main_menu)
        match choice:
            case 1:
                play_game()
            case 2:
                settings_menu()
            case 3:
                close()


def play_game(clear=True) -> None:
    if clear:
        clear_screen()

    category, words = choice(list(WORDS[SETTINGS['words']].items()))
    word = choice(words)
    under_str = '_' * len(word)

    part, clue = None, None
    match SETTINGS["difficulty"]:
        case 'easy':
            part = 0
            clue = category
        case 'normal':
            part = 2
            clue = category
        case 'hard':
            part = 3

    while True:
        clear_screen()
        print_hangman(part, Fore.MAGENTA)
        if part == 9:
            print(Fore.BLACK + Back.RED + 'You Loose!')
            sleep(4)
            break

        if clue:
            print(Fore.CYAN + clue + ':')
        print(Fore.GREEN + under_str + '\n')

        letter = input(Style.BRIGHT + Fore.YELLOW +
                       '  -->   ' + Fore.GREEN)[0].upper()
        if letter not in word:
            part += 1
        else:
            for i in range(len(word)):
                if letter == word[i]:
                    under_str = under_str[:i] + letter + under_str[i+1:]
        if under_str == word:
            clear_screen()
            print(Fore.BLUE + Back.GREEN + 'You Win!')
            sleep(3)
            break
    main_menu()


def settings_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('', TRANSLATIONS["settings"], 1, Fore.CYAN)
    print_txt(
        '> (1) | ', f'{TRANSLATIONS["lng_words"]}\t| {SETTINGS["words"]}')
    print_txt(
        '> (2) | ', f'{TRANSLATIONS["language"]}\t| {SETTINGS["language"]}')
    print_txt(
        '> (3) | ', f'{TRANSLATIONS["difficulty"]}\t| {SETTINGS["difficulty"]}')
    print_txt(
        '> (4) | ', TRANSLATIONS["back"], 1)
    if inp:
        choice = input_choice((1, 2, 3, 4), settings_menu)
        match choice:
            case 1:
                words_menu()
            case 2:
                language_menu()
            case 3:
                difficulty_menu()
            case 4:
                main_menu()


def words_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('', TRANSLATIONS["lng_words"], 1, Fore.CYAN)
    print_txt(
        '> (1) | ', f'{TRANSLATIONS["lng_choose"]}\t| {SETTINGS["words"]}')
    print_txt('> (2) | ', TRANSLATIONS["add_word"])
    print_txt('> (3) | ', TRANSLATIONS["del_word"])
    print_txt('> (4) | ', TRANSLATIONS["back"], 1)
    if inp:
        choice = input_choice((1, 2, 3, 4), words_menu)
        match choice:
            case 1:
                lng_words_menu()
            case 2:
                add_word_menu()
            case 3:
                del_word_menu()
                pass
            case 4:
                settings_menu()


def print_lng() -> None:
    print_txt('> (1) | ', 'ru')
    print_txt('> (2) | ', 'en')
    print_txt('> (3) | ', TRANSLATIONS["back"], 1)


def language_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('', TRANSLATIONS["language"], 1, Fore.CYAN)
    print_lng()
    if inp:
        choice = input_choice((1, 2, 3), language_menu)
        if choice == 3:
            settings_menu()
        else:
            SETTINGS['language'] = 'ru' if choice == 1 else 'en'
            init_settings(mode='w')
            init_translations(SETTINGS['language'])
            main_menu()


def difficulty_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('', TRANSLATIONS["difficulty"], 1, Fore.CYAN)
    print_txt('> (1) | ', TRANSLATIONS["easy"])
    print_txt('> (2) | ', TRANSLATIONS["normal"])
    print_txt('> (3) | ', TRANSLATIONS["hard"])
    print_txt('> (4) | ', TRANSLATIONS["back"], 1)
    if inp:
        choice = input_choice((1, 2, 3, 4), difficulty_menu)
        match choice:
            case 1:
                SETTINGS['difficulty'] = 'easy'
            case 2:
                SETTINGS['difficulty'] = 'normal'
            case 3:
                SETTINGS['difficulty'] = 'hard'
        if choice == 4:
            settings_menu()
        else:
            init_settings(mode='w')
            main_menu()


def lng_words_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('', TRANSLATIONS["lng_choose"], 1, Fore.CYAN)
    print_lng()
    if inp:
        choice = input_choice((1, 2, 3), lng_words_menu)
        if choice == 3:
            words_menu()
        else:
            SETTINGS['words'] = 'ru' if choice == 1 else 'en'
            init_settings(mode='w')
            main_menu()


def add_word_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('', TRANSLATIONS["add_word"], 1, Fore.CYAN)
    print_lng()
    if inp:
        choice = input_choice((1, 2, 3), add_word_menu)
        print_txt('', TRANSLATIONS["warning_add"], 1, Fore.RED)
        if choice == 3:
            words_menu()
        else:
            lng = 'ru' if choice == 1 else 'en'
            category = input(Style.BRIGHT + Fore.YELLOW + '  -->   ' +
                             Fore.MAGENTA + f'{TRANSLATIONS["category"]}: ' +
                             Fore.GREEN).upper()
            word = input(Style.BRIGHT + Fore.YELLOW + '  -->   ' +
                         Fore.MAGENTA + f'{TRANSLATIONS["word"]}: ' +
                         Fore.GREEN).upper()
            WORDS[lng].setdefault(category, []).append(word)
            init_json(mode='w')
            main_menu()


def del_word_menu(clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt('', TRANSLATIONS["del_word"], 1, Fore.CYAN)
    print_lng()
    if inp:
        choice = input_choice((1, 2, 3), add_word_menu)
        if choice == 3:
            words_menu()
        else:
            choice_del_word('ru' if choice == 1 else 'en')


def choice_del_word(lng: str, clear=True, inp=True) -> None:
    if clear:
        clear_screen()
    print_txt(f'{TRANSLATIONS["del_word"]} -> ', f'{lng}:', 1, Fore.CYAN)
    i = 1
    for category, words in WORDS[lng].items():
        print_txt(f'> ({i})\t', f'{category}:', 1, Fore.CYAN)
        for word in words:
            i += 1
            print_txt(f'> \t ({i})  ', f'{word}', 1, Fore.MAGENTA)
        i += 1
    print_txt(f'> (0) ', TRANSLATIONS["back"], 1)
    if inp:
        choice = input_choice(range(i))
        if choice == 0:
            words_menu()
        else:
            i = 0
            for category, words in WORDS[lng].items():
                i += 1
                if choice == i:
                    del WORDS[lng][category]
                    break
                for word in words:
                    i += 1
                    if choice == i:
                        WORDS[lng][category].remove(word)
                        if len(WORDS[lng][category]) == 0:
                            del WORDS[lng][category]
                        break
                else:
                    continue
                break
            init_json(mode='w')
            main_menu()


def main() -> None:
    clear_screen()
    init_json()
    init_settings()
    init_translations(SETTINGS['language'])
    print_intro()
    main_menu(clear=False)


if __name__ == "__main__":
    main()
