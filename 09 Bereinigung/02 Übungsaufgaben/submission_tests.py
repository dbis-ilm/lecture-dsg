import os

import numpy as np
import pandas as pd
from jptest2 import *


# Datensatz verändern
@JPPreRun
async def pre():
    df = pd.read_csv('disney_plus_titles.csv')
    df = df.sample(frac=0.67, random_state=384)
    df.to_pickle('dpt.pickle')


@JPPostRun
async def post():
    if os.path.exists('dpt.pickle'):
        os.remove('dpt.pickle')


# Imports und Daten laden
# noinspection PyUnresolvedReferences
def imports():
    import pandas as pd
    import numpy as np


def load_csv():
    df = pd.read_csv('disney_plus_titles.csv')


def load_pickle():
    df = pd.read_pickle('dpt.pickle')


# Aufgabe 1
@JPTestComparison('Aufgabe 1', max_score=1, prepare=imports,
                  execute_left=('task-1',), hold_left='df',
                  execute_right=load_csv, hold_right='df')
async def aufgabe1(result, test):
    yield test.equals(result), 1


# Aufgabe 2
def aufgabe2_solution(df):
    df['type'] = df['tmdb_ref'].str.split('/').str[1].replace({
        'movie': 'Movie',
        'tv': 'TV Show'
    })


@JPTestComparison('Aufgabe 2', max_score=2, prepare=[imports, load_pickle],
                  execute_left=('task-2',), hold_left='df_type',
                  execute_right=aufgabe2_solution, hold_right='df')
async def aufgabe2(result, test):
    yield test.equals(result), 2


# Aufgabe 3
def aufgabe3_solution(df):
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


@JPTestComparison('Aufgabe 3', max_score=2,
                  prepare=[imports, load_pickle],
                  execute_left=('task-3',), hold_left='df_release',
                  execute_right=aufgabe3_solution, hold_right='df')
async def aufgabe3(result, test):
    yield test.equals(result), 2


# Aufgabe 4
def aufgabe4_solution(df: pd.DataFrame):
    df['revenue'] = df['revenue'].replace(0, np.nan)
    df['revenue'] = pd.cut(df['revenue'],
                           [0, 40_000_000, 400_000_000, df['revenue'].max()],
                           labels=['niedrig', 'mittel', 'hoch'])
    df['revenue'] = df['revenue'].cat.add_categories(['unbekannt']).fillna('unbekannt')


@JPTestComparison('Aufgabe 4', max_score=2,
                  prepare=[imports, load_pickle],
                  execute_left=('task-4',), hold_left='df_grouped',
                  execute_right=aufgabe4_solution, hold_right='df')
async def aufgabe4(result, test):
    yield test.equals(result), 2


# Aufgabe 5
def aufgabe5_solution(df: pd.DataFrame):
    df['runtime'] = df['runtime'].replace(0, np.nan)
    df['episode_count'] = df['episode_count'].fillna(1)
    df['avg_runtime'] = df['runtime'] / df['episode_count']

    result = df.groupby('type')['avg_runtime'].mean()

    avg_movie_runtime = result['Movie']
    avg_tvshow_runtime = result['TV Show']


@JPTestComparison('Aufgabe 5', max_score=2,
                  prepare=[imports, load_pickle],
                  execute_left=('task-5',), hold_left=['avg_movie_runtime', 'avg_tvshow_runtime'],
                  execute_right=aufgabe5_solution, hold_right=['avg_movie_runtime', 'avg_tvshow_runtime'], )
async def aufgabe5(result_movie, result_tv, test_movie, test_tv):
    yield abs(test_movie - result_movie) < 1e-6, 1, 'avg_movie_runtime'
    yield abs(test_tv - result_tv) < 1e-6, 1, 'avg_tvshow_runtime'


# Aufgabe 6
def aufgabe6_solution(df: pd.DataFrame):
    min_value = df['popularity'].min()
    max_value = df['popularity'].max()
    df['popularity'] = (df['popularity'] - min_value) / (max_value - min_value) * 100


@JPTestComparison('Aufgabe 6', max_score=2,
                  prepare=[imports, load_pickle],
                  execute_left=('task-6',), hold_left=['df_normalized'],
                  execute_right=aufgabe6_solution, hold_right='df')
async def aufgabe6(result, test):
    yield test.equals(result), 2
