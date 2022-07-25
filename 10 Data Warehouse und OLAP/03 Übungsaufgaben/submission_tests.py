import os

import pandas as pd
from jptest import *

# Imports
imports = '''
    import pandas as pd
'''

# Datensatz vorbereiten
load_data = 'df = pd.read_pickle("dpt.pickle")'


@JPPreRun
def pre():
    # read data
    df: pd.DataFrame = pd.read_csv('disney_plus_titles.csv')

    # sample
    df = df.sample(frac=0.67, random_state=768)

    # add `avg_runtime` columns and replace NaN
    df['avg_runtime'] = df['runtime'] / df['episode_count'].fillna(1)

    # store pickled
    df.to_pickle('dpt.pickle')


@JPPostRun
def post():
    if os.path.exists('dpt.pickle'):
        os.remove('dpt.pickle')


# Aufgabe 1
@JPTest('Aufgabe 1', max_score=1, execute=[imports, ('task-1',)])
def aufgabe1(tb: JPTestBook):
    result = tb.get('df')
    test = tb.inject('''
        df = pd.read_csv('disney_plus_titles.csv')
        df['avg_runtime'] = df['runtime'] / df['episode_count'].fillna(1)
    ''', 'df')

    yield test.equals(result), 1


# Aufgabe 2
aufgabe2_solution = [
    '''
        df_discrete = df.copy()
        
        df_discrete['release'] = df_discrete['release'].str[:7]
        df_discrete['avg_runtime'] = pd.cut(df_discrete['avg_runtime'],
                                            (0, 30, 70, df_discrete['avg_runtime'].max()),
                                            labels=('kurz', 'mittel', 'lang'))                                   
    ''',
    '''
        result_cube = df_discrete.groupby(['release', 'avg_runtime', 'episode_count', 'type'])['popularity'].max()
    '''
]


@JPTest('Aufgabe 2', max_score=2, execute=[imports, load_data, ('task-2',)])
def aufgabe2(tb: JPTestBook):
    df_result = tb.get('df_discrete')
    cube_result = tb.get('result_cube')

    tb.inject(load_data)

    df_test = tb.inject(aufgabe2_solution[0], 'df_discrete')
    yield df_test.equals(df_result), 1, 'df_discrete'

    cube_test = tb.inject(aufgabe2_solution[1], 'result_cube')
    yield cube_test.equals(cube_result), 1, 'result_cube'


# Aufgabe 3
aufgabe3_solution = '''
    rotated_cube = result_cube.swaplevel(i=0, j=1).swaplevel(i=0, j=3)
'''


@JPTest('Aufgabe 3', max_score=1, execute=[imports, load_data,
                                           aufgabe2_solution,
                                           ('task-3',)])
def aufgabe3(tb: JPTestBook):
    result = tb.get('rotated_cube')

    tb.inject(load_data)
    tb.inject(aufgabe2_solution[0])
    tb.inject(aufgabe2_solution[1])

    test = tb.inject(aufgabe3_solution, 'rotated_cube')

    yield test.equals(result), 1


# Aufgabe 4
aufgabe4_solution = '''
    sliced_cube = rotated_cube['TV Show']
'''


@JPTest('Aufgabe 4', max_score=1, execute=[imports, load_data,
                                           aufgabe2_solution, aufgabe3_solution,
                                           ('task-4',)])
def aufgabe4(tb: JPTestBook):
    result = tb.get('sliced_cube')

    tb.inject(load_data)
    tb.inject(aufgabe2_solution[0])
    tb.inject(aufgabe2_solution[1])
    tb.inject(aufgabe3_solution)

    test = tb.inject(aufgabe4_solution, 'sliced_cube')

    yield test.equals(result), 1


# Aufgabe 5
aufgabe5_solution = '''
    rolled_cube = sliced_cube.groupby([lambda x: x[0][:4], 'episode_count', 'avg_runtime']).max()
'''


@JPTest('Aufgabe 5', max_score=1, execute=[imports, load_data,
                                           aufgabe2_solution, aufgabe3_solution, aufgabe4_solution,
                                           ('task-5',)])
def aufgabe5(tb: JPTestBook):
    result = tb.get('rolled_cube')

    tb.inject(load_data)
    tb.inject(aufgabe2_solution[0])
    tb.inject(aufgabe2_solution[1])
    tb.inject(aufgabe3_solution)
    tb.inject(aufgabe4_solution)

    test = tb.inject(aufgabe5_solution, 'rolled_cube')

    yield test.equals(result), 1

