import json
from os import path, replace
from shutil import copyfile

from jptest2 import *


# noinspection PyUnresolvedReferences
def imports():
    import csv
    import json


@JPSetup
async def remove_some_actors():
    if not path.exists('disney_plus_titles.json.bak'):
        copyfile('disney_plus_titles.json', 'disney_plus_titles.json.bak')

    with open('disney_plus_titles.json') as file:
        json_data = json.load(file)

    for line in json_data:
        if 'Jim Cummings' in line['cast']:
            line['cast'].remove('Jim Cummings')
        if 'Walt Disney' in line['cast']:
            line['cast'].remove('Walt Disney')

    with open('disney_plus_titles.json', 'w') as file:
        json.dump(json_data, file)


@JPTeardown
async def add_some_actors():
    replace('disney_plus_titles.json.bak', 'disney_plus_titles.json')


# Aufgabe 1
def task1_solution():
    with open('disney_plus_titles.csv') as file:
        csv_data = list(csv.reader(file))

    releases_per_year = {}

    for _, year in csv_data[1:]:
        if year in releases_per_year:
            releases_per_year[year] += 1
        else:
            releases_per_year[year] = 1


@JPTestComparison('Aufgabe 1', max_score=2,
                  execute_left=[imports, ('task-1',)], hold_left=['csv_data', 'releases_per_year'],
                  execute_right=[imports, task1_solution], hold_right=['csv_data', 'releases_per_year'])
async def task1(csv_data_result, releases_per_year_result, csv_data_test, releases_per_year_test):
    yield any([
        csv_data_result == csv_data_test,
        csv_data_result == csv_data_test[1:]
    ]), 1, 'Laden des Datensatzes nicht korrekt'

    yield releases_per_year_result == releases_per_year_test, 1, 'Dictionary nicht korrekt'


# Aufgabe 2
def task2_solution():
    with open('disney_plus_titles.json') as file:
        json_data = json.load(file)


@JPTestComparison('Aufgabe 2', max_score=2,
                  execute_left=[imports, ('task-2',)], hold_left=['json_data', 'most_frequent_actor'],
                  execute_right=[imports, task2_solution], hold_right='json_data')
async def task2(data_result, most_frequent_actor_result, data_test):
    yield data_result == data_test, 1, 'Laden des Datensatzes nicht korrekt'
    yield most_frequent_actor_result == 'Bill Farmer', 1, 'Schauspieler nicht korrekt'
