import asyncio
import os

import numpy.random
import numpy.random
import pandas as pd
from jptest2 import *
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score


# Vorbereitungen
# noinspection PyUnresolvedReferences
def imports():
    import numpy.random

    import pandas as pd
    import plotly.express as px

    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.metrics import silhouette_score


def load_pickle():
    df = pd.read_pickle("df.pickle")


def init_rnd():
    numpy.random.seed(16)


@JPPreRun
async def pre():
    # read data
    df: pd.DataFrame = pd.read_csv('clustering.csv')

    mva_min, mva_max = df['movie_vote_average'].min(), df['movie_vote_average'].max()
    df['movie_vote_average'] = (df['movie_vote_average'] - mva_min) / (mva_max - mva_min)

    # shuffle movie_vote_average column
    df['movie_vote_average'] = df['movie_vote_average'].sample(frac=1, random_state=312).reset_index(drop=True)

    # store pickled
    df.to_pickle('df.pickle')


@JPPostRun
async def post():
    if os.path.exists('df.pickle'):
        os.remove('df.pickle')


# Aufgabe 1
def aufgabe1_solution():
    df = pd.read_csv('clustering.csv')

    mva_min, mva_max = df['movie_vote_average'].min(), df['movie_vote_average'].max()
    df['movie_vote_average'] = (df['movie_vote_average'] - mva_min) / (mva_max - mva_min)


@JPTest('Aufgabe 1', max_score=2, execute=imports, prepare_second=True)
async def aufgabe1(left: Notebook, right: Notebook):
    # track plotly calls
    async with left.track_fun('px.scatter', 'x', 'y') as params:
        # execute user code and sample solution
        await asyncio.gather(
            left.execute_cells('task-1'),
            right.execute_fun(aufgabe1_solution)
        )

        # store call
        call = await params.receive_last()

    # receive
    result, test = await asyncio.gather(
        left.ref('df').receive(),
        right.ref('df').receive()
    )

    # compare
    yield test.equals(result), 1, 'DataFrame nicht korrekt geladen'

    yield 'x' in call and 'y' in call and (
            (
                    call.x == 'adult_ratio' and call.y == 'movie_vote_average'
            ) or (
                    call.x == 'movie_vote_average' and call.y == 'adult_ratio'
            )
    ), 1, 'Aufruf des Graphs nicht korrekt'


# Aufgabe 2
def aufgabe2_solution(df: pd.DataFrame, n_clusters: int):
    df['kmeans'] = KMeans(n_clusters).fit_predict(df[['adult_ratio', 'movie_vote_average']])


@JPTest('Aufgabe 2', max_score=2, execute=[imports, load_pickle, init_rnd], prepare_second=True)
async def aufgabe2(left: Notebook, right: Notebook):
    # execute user code and find value for `n_clusters`
    async with left.track_fun('KMeans', 'n_clusters') as params:
        await left.execute_cells('task-2')
        n_clusters = (await params.receive_last()).n_clusters

    # execute sample solution with `n_clusters` as parameter
    await right.store('n_clusters', n_clusters)
    await right.execute_fun(aufgabe2_solution)

    # receive
    result, test = await asyncio.gather(
        left.ref('df').receive(),
        right.ref('df').receive()
    )
    test = await right.ref('df').receive()

    # compare
    yield test.equals(result), 2


# Aufgabe 3
def aufgabe3_solution(df: pd.DataFrame, eps, min_samples):
    df['dbscan'] = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(df[['adult_ratio', 'movie_vote_average']])


@JPTest('Aufgabe 3', max_score=2, execute=[imports, load_pickle, init_rnd], prepare_second=True)
async def aufgabe3(left: Notebook, right: Notebook):
    # execute user code and find value for `n_clusters`
    async with left.track_fun('DBSCAN', 'eps', 'min_samples') as params:
        await left.execute_cells('task-3')
        eps = (await params.receive_last()).eps
        min_samples = (await params.receive_last()).min_samples

    # execute sample solution with `n_clusters` as parameter
    await right.store('eps', eps)
    await right.store('min_samples', min_samples)
    await right.execute_fun(aufgabe3_solution)

    # receive
    result, test = await asyncio.gather(
        left.ref('df').receive(),
        right.ref('df').receive()
    )
    test = await right.ref('df').receive()

    # compare
    yield test.equals(result), 2


# Aufgabe 4
def aufgabe4_preparation(df: pd.DataFrame):
    df['kmeans'] = KMeans(4).fit_predict(df[['adult_ratio', 'movie_vote_average']])
    df['dbscan'] = DBSCAN(eps=0.15, min_samples=3).fit_predict(df[['adult_ratio', 'movie_vote_average']])


def aufgabe4_solution(df: pd.DataFrame):
    kmeans_silhouette = silhouette_score(df[['adult_ratio', 'movie_vote_average']], df['kmeans'])
    dbscan_silhouette = silhouette_score(df[['adult_ratio', 'movie_vote_average']], df['dbscan'])


@JPTest('Aufgabe 4', max_score=2, execute=[imports, load_pickle, init_rnd, aufgabe4_preparation], prepare_second=True)
async def aufgabe4(left: Notebook, right: Notebook):
    await asyncio.gather(
        left.execute_cells('task-4'),
        right.execute_fun(aufgabe4_solution)
    )

    result_kmeans, result_dbscan, test_kmeans, test_dbscan = await asyncio.gather(
        left.ref('kmeans_silhouette').receive(),
        left.ref('dbscan_silhouette').receive(),
        right.ref('kmeans_silhouette').receive(),
        right.ref('dbscan_silhouette').receive(),
    )

    yield abs(test_kmeans - result_kmeans) < 1e-7, 1
    yield abs(test_dbscan - result_dbscan) < 1e-7, 1
