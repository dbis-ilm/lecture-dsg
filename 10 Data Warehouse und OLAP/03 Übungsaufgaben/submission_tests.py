import os

import pandas as pd
from jptest2 import *


# Imports und Daten laden
def imports():
    # noinspection PyUnresolvedReferences
    import pandas as pd


def load_pickle():
    df = pd.read_pickle("dpt.pickle")


# Datensatz vorbereiten
@JPPreRun
async def pre():
    # read data
    df: pd.DataFrame = pd.read_csv('disney_plus_titles.csv')

    # sample
    df = df.sample(frac=0.67, random_state=768)

    # add `avg_runtime` columns and replace NaN
    df['avg_runtime'] = df['runtime'] / df['episode_count'].fillna(1)

    # store pickled
    df.to_pickle('dpt.pickle')


@JPPostRun
async def post():
    if os.path.exists('dpt.pickle'):
        os.remove('dpt.pickle')


# Aufgabe 1
def aufgabe1_solution():
    df = pd.read_csv('disney_plus_titles.csv')
    df['avg_runtime'] = df['runtime'] / df['episode_count'].fillna(1)


@JPTestComparison('Aufgabe 1', max_score=1,
                  prepare=[imports],
                  execute_left=('task-1',), hold_left='df',
                  execute_right=aufgabe1_solution, hold_right='df')
async def aufgabe1(result, test):
    yield test.equals(result), 1


# Aufgabe 2
def aufgabe2_solution(df: pd.DataFrame):
    df_discrete = df.copy()

    df_discrete['release'] = df_discrete['release'].str[:7]
    df_discrete['avg_runtime'] = pd.cut(df_discrete['avg_runtime'],
                                        (0, 30, 70, df_discrete['avg_runtime'].max()),
                                        labels=('kurz', 'mittel', 'lang'))

    result_cube = df_discrete.groupby(['release', 'avg_runtime', 'episode_count', 'type'])['popularity'].max()


@JPTestComparison('Aufgabe 2', max_score=2,
                  prepare=[imports, load_pickle],
                  execute_left=('task-2',), hold_left=['df_discrete', 'result_cube'],
                  execute_right=aufgabe2_solution, hold_right=['df_discrete', 'result_cube'])
async def aufgabe2(df_result, cube_result, df_test, cube_test):
    yield df_test.equals(df_result), 1, 'df_discrete'
    yield cube_test.equals(cube_result), 1, 'result_cube'


# Aufgabe 3
def aufgabe3_solution(result_cube: pd.Series):
    rotated_cube = result_cube.swaplevel(i=0, j=1).swaplevel(i=0, j=3)


@JPTestComparison('Aufgabe 3', max_score=1,
                  prepare=[imports, load_pickle, aufgabe2_solution],
                  execute_left=('task-3',), hold_left='rotated_cube',
                  execute_right=aufgabe3_solution, hold_right='rotated_cube')
async def aufgabe3(result, test):
    yield test.equals(result), 1


# Aufgabe 4
def aufgabe4_solution(rotated_cube: pd.Series):
    sliced_cube = rotated_cube['TV Show']


@JPTestComparison('Aufgabe 4', max_score=1,
                  prepare=[imports, load_pickle, aufgabe2_solution, aufgabe3_solution],
                  execute_left=('task-4',), hold_left='sliced_cube',
                  execute_right=aufgabe4_solution, hold_right='sliced_cube')
async def aufgabe4(result, test):
    yield test.equals(result), 1


# Aufgabe 5
def aufgabe5_solution(sliced_cube: pd.Series):
    rolled_cube = sliced_cube.groupby([lambda x: x[0][:4], 'episode_count', 'avg_runtime']).max()


@JPTestComparison('Aufgabe 5', max_score=1,
                  prepare=[imports, load_pickle, aufgabe2_solution, aufgabe3_solution, aufgabe4_solution],
                  execute_left=('task-5',), hold_left='rolled_cube',
                  execute_right=aufgabe5_solution, hold_right='rolled_cube')
async def aufgabe5(result, test):
    yield test.equals(result), 1
