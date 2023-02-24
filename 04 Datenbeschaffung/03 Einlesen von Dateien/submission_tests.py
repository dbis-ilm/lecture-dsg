from os import path, replace
from shutil import copyfile
from string import ascii_letters

from jptest2 import *


@JPSetup
async def add_duplicated_entries():
    if not path.exists('disney_plus_titles_jun22.txt.bak'):
        copyfile('disney_plus_titles_jun22.txt', 'disney_plus_titles_jun22.txt.bak')

    with open('disney_plus_titles_jun22.txt', 'r') as file:
        data = file.readlines()

    for i in range(94):
        data.insert(12 * i + 1, data[15 * i + 3])

    with open('disney_plus_titles_jun22.txt', 'w') as file:
        file.writelines(data)


@JPTeardown
async def remove_duplicated_entries():
    replace('disney_plus_titles_jun22.txt.bak', 'disney_plus_titles_jun22.txt')


# Aufgabe 1
def task1_solution():
    letters = {}

    with open('disney_plus_titles_jun22.txt') as file:
        for line in file:
            for character in line:
                if character.isalpha():
                    if character in letters:
                        letters[character] += 1
                    else:
                        letters[character] = 1


@JPTestComparison('Aufgabe 1', max_score=1,
                  execute_left=('task-1',), hold_left='letters',
                  execute_right=task1_solution, hold_right='letters')
async def task1(result, test):
    wrong = []
    for letter in ascii_letters:
        if test[letter] != result[letter]:
            wrong.append(letter)

    yield len(wrong) == 0, 1, f'Abweichung bei Buchstabe(n) {",".join(wrong)}'


# Aufgabe 2
def task2_solution():
    titles = set()
    lines = 0

    with open('disney_plus_titles_jun22.txt') as file:
        for line in file:
            titles.add(line.strip())
            lines += 1

    number_of_duplicate_entries = lines - len(titles)


@JPTestComparison('Aufgabe 2', max_score=1,
                  execute_left=('task-2',), hold_left='number_of_duplicate_entries',
                  execute_right=task2_solution, hold_right='number_of_duplicate_entries')
async def task2(result, test):
    yield test == result, 1
