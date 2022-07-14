from os import path, replace
from shutil import copyfile

from jptest import *
from string import ascii_letters


@JPPreRun
def add_duplicated_entries():
    if not path.exists('disney_plus_titles_jun22.txt.bak'):
        copyfile('disney_plus_titles_jun22.txt', 'disney_plus_titles_jun22.txt.bak')

    with open('disney_plus_titles_jun22.txt', 'r') as file:
        data = file.readlines()

    for i in range(94):
        data.insert(12 * i + 1, data[15 * i + 3])

    with open('disney_plus_titles_jun22.txt', 'w') as file:
        file.writelines(data)


@JPPostRun
def remove_duplicated_entries():
    replace('disney_plus_titles_jun22.txt.bak', 'disney_plus_titles_jun22.txt')


@JPTest('Aufgabe 1', max_score=1, execute=('task-1',))
def task1(tb: JPTestBook):
    result = tb.get('letters')
    test = tb.inject('''
        letters = {}

        with open('disney_plus_titles_jun22.txt') as file:
            for line in file:
                for character in line:
                    if character.isalpha():
                        if character in letters:
                            letters[character] += 1
                        else:
                            letters[character] = 1
    ''', 'letters')

    wrong = []
    for letter in ascii_letters:
        if test[letter] != result[letter]:
            wrong.append(letter)

    yield len(wrong) == 0, 1, f'Abweichung bei Buchstabe(n) {",".join(wrong)}'


@JPTest('Aufgabe 2', max_score=1, execute=('task-2',))
def task2(tb: JPTestBook):
    result = tb.get('number_of_duplicate_entries')
    test = tb.inject('''
        titles = set()
        lines = 0

        with open('disney_plus_titles_jun22.txt') as file:
            for line in file:
                titles.add(line.strip())
                lines += 1

        number_of_duplicate_entries = lines - len(titles)
    ''', 'number_of_duplicate_entries')

    yield test == result, 1
