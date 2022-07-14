from jptest import *
import os
import pandas as pd
from random import shuffle

# Vorbereitungen
imports = 'import pandas as pd'
load_data = 'df = pd.read_pickle("dpt.pickle")'


@JPPreRun
def pre():
    # read data
    df: pd.DataFrame = pd.read_csv('disney_plus_titles.csv')

    # sample
    df = df.sample(frac=0.67, random_state=512)

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
    ''', 'df')

    yield test.equals(result), 1


# Aufgabe 2
@JPTest('Aufgabe 2', max_score=1, execute=[imports, load_data, ('task-2-1',), ('task-2-2',)])
def aufgabe2(tb: JPTestBook):
    result = tb.get('df')
    test = tb.inject(f'''
        {load_data}
        df['release_after_2000'] = df['release_year'] >= 2000
        df.drop('duration', axis=1, inplace=True)
    ''', 'df')

    yield test.equals(result), 1


# Aufgabe 3
@JPTest('Aufgabe 3', max_score=1, execute=[imports, load_data, ('task-3',)])
def aufgabe3(tb: JPTestBook):
    result_movie, result_tv = tb.get('rel_movie_count', 'rel_tvshow_count')
    test_movie, test_tv = tb.inject(f'''
        {load_data}
        
        count = df.groupby('type').size()
        abs_movie_count = count['Movie']
        abs_tvshow_count = count['TV Show']
        
        rel_movie_count = abs_movie_count / (abs_movie_count + abs_tvshow_count)
        rel_tvshow_count = abs_tvshow_count / (abs_movie_count + abs_tvshow_count)
    ''', 'rel_movie_count', 'rel_tvshow_count')

    yield test_movie == result_movie, 0.5
    yield test_tv == result_tv, 0.5


# Aufgabe 4
@JPTest('Aufgabe 4', max_score=3, execute=[imports, load_data, ('task-4',)])
def aufgabe4(tb: JPTestBook):
    tb.inject(load_data)

    # df_directors
    result = tb.get('df_directors')
    test = tb.inject('''
        series = df['director'].str.split(', ', expand=True).stack().reset_index(level=[1], drop=True)
        df_directors = series.rename('director').to_frame()
    ''', 'df_directors')

    yield test.equals(result), 1, 'df_directors'

    # df_directors_with_titles
    result = tb.get('df_directors_with_titles')
    test = tb.inject('''
        df_titles_only = df[['title']]
        df_directors_with_titles = pd.merge(df_directors, df_titles_only, left_index=True, right_index=True)
    ''', 'df_directors_with_titles')

    yield test.equals(result), 1, 'df_directors_with_titles'

    # df_result
    result = tb.get('df_result')
    test = tb.inject('''
        df_result = df_directors_with_titles.groupby('director').agg({'title': lambda x: ', '.join(x)})
    ''', 'df_result')

    yield test.equals(result), 1, 'df_result'
