from jptest import *
import pandas as pd
import os

imports = '''
    import pandas as pd
    import numpy as np
'''


# Datensatz verändern
@JPPreRun
def pre():
    df = pd.read_csv('disney_plus_titles.csv')
    df = df.sample(frac=0.67, random_state=384)
    df.to_pickle('dpt.pickle')


@JPPostRun
def post():
    if os.path.exists('dpt.pickle'):
        os.remove('dpt.pickle')


def load(tb: JPTestBook):
    return tb.inject('''
        df = pd.read_pickle('dpt.pickle')
    ''', 'df')


# Aufgabe 1
@JPTest('Aufgabe 1', max_score=1, execute=[imports, ('task-1',)])
def aufgabe1(tb: JPTestBook):
    result = tb.get('df')
    test = tb.inject('''
        df = pd.read_csv('disney_plus_titles.csv')
    ''', 'df')

    yield test.equals(result), 1


# Aufgabe 2
@JPTest('Aufgabe 2', max_score=2, execute=[imports, load, ('task-2',)])
def aufgabe2(tb: JPTestBook):
    result = tb.get('df_type')

    load(tb)
    test = tb.inject('''
        df['type'] = df['tmdb_ref'].str.split('/').str[1].replace({
            'movie': 'Movie',
            'tv': 'TV Show'
        })
    ''', 'df')

    yield test.equals(result), 2


# Aufgabe 3
@JPTest('Aufgabe 3', max_score=2, execute=[imports, load, ('task-3',)])
def aufgabe3(tb: JPTestBook):
    result = tb.get('df_release')

    load(tb)
    test = tb.inject('''
        def to_yyyymmdd(x):
            if x is np.nan or isinstance(x, float):
                return x
            if len(x) == 10:
                return x
            
            year = int(x[:2])
            if year <= 30:
                year += 2000
            else:
                year += 1900
            
            return f'{year}-{x[2:]}'
            
        df['release'] = df['release'].map(to_yyyymmdd)
        df['release'] = pd.to_datetime(df['release'])
    ''', 'df')

    yield test.equals(result), 2


# Aufgabe 4
@JPTest('Aufgabe 4', max_score=2, execute=[imports, load, ('task-4',)])
def aufgabe4(tb: JPTestBook):
    result = tb.get('df_grouped')

    load(tb)
    test = tb.inject('''
        df['revenue'] = df['revenue'].replace(0, np.nan)
        df['revenue'] = pd.cut(df['revenue'],
                               [0, 40_000_000, 400_000_000, df['revenue'].max()],
                               labels=['niedrig', 'mittel', 'hoch'])
        df['revenue'] = df['revenue'].cat.add_categories(['unbekannt']).fillna('unbekannt')
    ''', 'df')

    yield test.equals(result), 2


# Aufgabe 5
@JPTest('Aufgabe 5', max_score=2, execute=[imports, load, ('task-5',)])
def aufgabe5(tb: JPTestBook):
    result_movie, result_tv = tb.get('avg_movie_runtime', 'avg_tvshow_runtime')

    load(tb)
    test_movie, test_tv = tb.inject('''
        df['runtime'] = df['runtime'].replace(0, np.nan)
        df['episode_count'] = df['episode_count'].fillna(1)
        df['avg_runtime'] = df['runtime'] / df['episode_count']
        
        result = df.groupby('type')['avg_runtime'].mean()
        
        avg_movie_runtime = result['Movie']
        avg_tvshow_runtime = result['TV Show']
    ''', 'avg_movie_runtime', 'avg_tvshow_runtime')

    yield abs(test_movie - result_movie) < 1e-6, 1, 'avg_movie_runtime'
    yield abs(test_tv - result_tv) < 1e-6, 1, 'avg_tvshow_runtime'


# Aufgabe 6
@JPTest('Aufgabe 6', max_score=2, execute=[imports, load, ('task-6',)])
def aufgabe6(tb: JPTestBook):
    result = tb.get('df_normalized')

    load(tb)
    test = tb.inject('''
        min_value = df['popularity'].min()
        max_value = df['popularity'].max()
        df['popularity'] = (df['popularity'] - min_value) / (max_value - min_value) * 100
    ''', 'df')

    yield test.equals(result), 2
