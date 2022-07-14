import json
from os import path, replace
from shutil import copyfile

from jptest import *

imports = '''
    import csv
    import json
'''


@JPPreRun
def remove_some_actors():
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


@JPPostRun
def add_some_actors():
    replace('disney_plus_titles.json.bak', 'disney_plus_titles.json')


@JPTest('Aufgabe 1', max_score=2, execute=[imports, ('task-1',)])
def task1(tb: JPTestBook):
    result = tb.get('csv_data')
    test = tb.inject('''
        with open('disney_plus_titles.csv') as file:
            csv_data = list(csv.reader(file))
    ''', 'csv_data')

    yield any([
        result == test,
        result == test[1:]
    ]), 1, 'Laden des Datensatzes nicht korrekt'

    result = tb.get('releases_per_year')
    test = tb.inject('''
        releases_per_year = {}

        for _, year in csv_data[1:]:
            if year in releases_per_year:
                releases_per_year[year] += 1
            else:
                releases_per_year[year] = 1
    ''', 'releases_per_year')

    yield result == test, 1, 'Dictionary nicht korrekt'


@JPTest('Aufgabe 2', max_score=2, execute=[imports, ('task-2',)])
def task2(tb: JPTestBook):
    result = tb.get('json_data')
    test = tb.inject('''
        with open('disney_plus_titles.json') as file:
            json_data = json.load(file)
    ''', 'json_data')

    yield result == test, 1, 'Laden des Datensatzes nicht korrekt'

    result = tb.get('most_frequent_actor')
    yield result == 'Bill Farmer', 1, 'Schauspieler nicht korrekt'
