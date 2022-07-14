from jptest import *

imports = 'import requests'


@JPTest('Aufgabe 1', max_score=1, execute=[imports, ('task-1',)])
def task1(tb: JPTestBook):
    result = tb.get('starships')

    yield all([
        len(result) == 5,
        'https://swapi.dev/api/starships/31/' in result,
        'https://swapi.dev/api/starships/32/' in result,
        'https://swapi.dev/api/starships/39/' in result,
        'https://swapi.dev/api/starships/40/' in result,
        'https://swapi.dev/api/starships/41/' in result
    ]), 1


@JPTest('Aufgabe 2', max_score=1, execute=[
    imports,
    '''
    starships = ['https://swapi.dev/api/starships/31/',
                 'https://swapi.dev/api/starships/32/',
                 'https://swapi.dev/api/starships/39/',
                 'https://swapi.dev/api/starships/40/',
                 'https://swapi.dev/api/starships/41/']
    ''',
    ('task-2',)
])
def task2(tb: JPTestBook):
    result = tb.get('starship_names')

    yield all([
        len(result) == 5,
        'Republic Cruiser' in result,
        'Droid control ship' in result,
        'Naboo fighter' in result,
        'Naboo Royal Starship' in result,
        'Scimitar' in result
    ]), 1
