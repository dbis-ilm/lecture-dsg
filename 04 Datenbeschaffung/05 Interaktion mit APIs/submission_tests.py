from jptest2 import *


# noinspection PyUnresolvedReferences
def imports():
    import requests


def starships():
    starships = ['https://swapi.dev/api/starships/31/',
                 'https://swapi.dev/api/starships/32/',
                 'https://swapi.dev/api/starships/39/',
                 'https://swapi.dev/api/starships/40/',
                 'https://swapi.dev/api/starships/41/']
    return starships


# Aufgabe 1
@JPTestGet('Aufgabe 1', max_score=1, execute=[imports, ('task-1',)], get='starships')
async def task1(result):
    yield all([
        len(result) == 5,
        *[s in result for s in starships()]
    ]), 1


# Aufgabe 2
@JPTestGet('Aufgabe 2', max_score=1, execute=[imports, starships, ('task-2',)], get='starship_names')
async def task2(result):
    yield all([
        len(result) == 5,
        'Republic Cruiser' in result,
        'Droid control ship' in result,
        'Naboo fighter' in result,
        'Naboo Royal Starship' in result,
        'Scimitar' in result
    ]), 1
