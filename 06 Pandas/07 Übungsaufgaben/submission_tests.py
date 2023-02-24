import os

import pandas as pd
from jptest2 import *


# Vorbereitungen
@JPSetup
async def pre():
    # read data
    df: pd.DataFrame = pd.read_csv('disney_plus_titles.csv')

    # sample
    df = df.sample(frac=0.67, random_state=512)

    # store pickled
    df.to_pickle('dpt.pickle')


@JPTeardown
async def post():
    if os.path.exists('dpt.pickle'):
        os.remove('dpt.pickle')


def imports():
    # noinspection PyUnresolvedReferences
    import pandas as pd


def load_data():
    df = pd.read_pickle("dpt.pickle")


# Aufgabe 1
def aufgabe1_solution():
    df = pd.read_csv('disney_plus_titles.csv')


@JPTestComparison('Aufgabe 1', max_score=1,
                  prepare=[imports],
                  hold_left='df', execute_left=('task-1',),
                  hold_right='df', execute_right=aufgabe1_solution)
async def aufgabe1(result, test):
    yield result.equals(test), 1


# Aufgabe 2
def aufgabe2_solution(df: pd.DataFrame):
    df['release_after_2000'] = df['release_year'] >= 2000
    df.drop('duration', axis=1, inplace=True)


@JPTestComparison('Aufgabe 2', max_score=1,
                  prepare=[imports, load_data],
                  hold_left='df', execute_left=[('task-2-1',), ('task-2-2',)],
                  hold_right='df', execute_right=aufgabe2_solution)
async def aufgabe2(result, test):
    yield test.equals(result), 1


# Aufgabe 3
def aufgabe3_solution(df: pd.DataFrame):
    count = df.groupby('type').size()
    abs_movie_count = count['Movie']
    abs_tvshow_count = count['TV Show']

    rel_movie_count = abs_movie_count / (abs_movie_count + abs_tvshow_count)
    rel_tvshow_count = abs_tvshow_count / (abs_movie_count + abs_tvshow_count)


@JPTestComparison('Aufgabe 3', max_score=1,
                  prepare=[imports, load_data],
                  hold_left=['rel_movie_count', 'rel_tvshow_count'], execute_left=('task-3',),
                  hold_right=['rel_movie_count', 'rel_tvshow_count'], execute_right=aufgabe3_solution)
async def aufgabe3(result_movie, result_tv, test_movie, test_tv):
    yield abs(test_movie - result_movie) < 1e-6, 0.5, 'rel_movie_count'
    yield abs(test_tv - result_tv) < 1e-6, 0.5, 'rel_tvshow_count'


# Aufgabe 4
def aufgabe4_solution(df: pd.DataFrame):
    # df_directors
    series = df['director'].str.split(', ', expand=True).stack().reset_index(level=[1], drop=True)
    df_directors = series.rename('director').to_frame()

    # df_directors_with_titles
    df_titles_only = df[['title']]
    df_directors_with_titles = pd.merge(df_directors, df_titles_only, left_index=True, right_index=True)

    # df_result
    df_result = df_directors_with_titles.groupby('director').agg({'title': lambda x: ', '.join(x)})


@JPTestComparison('Aufgabe 4', max_score=3,
                  prepare=[imports, load_data],
                  hold_left=['df_directors', 'df_directors_with_titles', 'df_result'], execute_left=('task-4',),
                  hold_right=['df_directors', 'df_directors_with_titles', 'df_result'], execute_right=aufgabe4_solution)
async def aufgabe4(result_df_directors, result_df_directors_with_titles, result_df_result,
                   test_df_directors, test_df_directors_with_titles, test_df_result):
    yield test_df_directors.equals(result_df_directors), 1, 'df_directors'
    yield test_df_directors_with_titles.equals(result_df_directors_with_titles), 1, 'df_directors_with_titles'
    yield test_df_result.equals(result_df_result), 1, 'df_result'
