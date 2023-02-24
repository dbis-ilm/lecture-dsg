import asyncio
import os
import random

import numpy as np
import pandas as pd
from jptest2 import *
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


# Vorbereitungen
# noinspection PyUnresolvedReferences
def imports():
    import pandas as pd

    import numpy as np
    import random

    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score, precision_score, recall_score


def load_pickle():
    df = pd.read_pickle("df.pickle")
    df_train, df_test = train_test_split(df, test_size=0.25)


def init_rnd():
    np.random.seed(14884)
    random.seed(14885)


@JPPreRun
async def pre():
    # lesen
    df: pd.DataFrame = pd.read_csv('classification_movies.csv')

    # alle Spalten normalisieren
    df_scaled = StandardScaler().fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)

    # `popular` invertieren
    df_scaled['popular'] = ~ df['popular']

    # store pickled
    df.to_pickle('df.pickle')


@JPPostRun
async def post():
    if os.path.exists('df.pickle'):
        os.remove('df.pickle')


# Aufgabe 1
def aufgabe1_solution():
    df = pd.read_csv('classification_movies.csv')
    df_train, df_test = train_test_split(df, test_size=0.25)


@JPTestComparison('Aufgabe 1', max_score=2,
                  prepare=[imports, init_rnd, load_pickle],
                  execute_left=('task-1',), hold_left=['df', 'df_train', 'df_test'],
                  execute_right=aufgabe1_solution, hold_right=['df', 'df_train', 'df_test'])
async def aufgabe1(result_df, result_df_train, result_df_test, test_df, test_df_train, test_df_test):
    yield test_df.equals(result_df), 1
    yield test_df_train.equals(result_df_train), 0.5
    yield test_df_test.equals(result_df_test), 0.5


# Aufgabe 2
def aufgabe2_solution(df_train: pd.DataFrame, df_test: pd.DataFrame, n_neighbors: int):
    X, y = df_train.drop('popular', axis=1), df_train['popular']
    nn = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, y)
    nn_accuracy = accuracy_score(df_test['popular'], nn.predict(df_test.drop('popular', axis=1)))


@JPTest('Aufgabe 2', max_score=2, execute=[imports, init_rnd, load_pickle], prepare_second=True)
async def aufgabe2(left: Notebook, right: Notebook):
    # result
    await left.execute_cells('task-2')
    result_nn = left.ref('nn')

    n_neighbors = await result_nn.n_neighbors.receive()

    # test
    await right.store('n_neighbors', n_neighbors)
    await right.execute_fun(aufgabe2_solution)

    test_nn = right.ref('nn')

    # compare predictions
    async def predict(nb: Notebook, nn: KNeighborsClassifier):
        df_test_y = await nb.ref('df_test').drop('popular', axis=1)
        prediction = await nn.predict(df_test_y)
        return await prediction.receive()

    result_pred, test_pred = await asyncio.gather(
        predict(left, result_nn),
        predict(right, test_nn)
    )

    yield np.array_equal(test_pred, result_pred), 1

    # compare accuracy
    result_accuracy, test_accuracy = await asyncio.gather(
        left.ref('nn_accuracy').receive(),
        right.ref('nn_accuracy').receive()
    )

    yield abs(test_accuracy - result_accuracy) < 1e-6, 1


# Aufgabe 3
def aufgabe3_solution(df_train: pd.DataFrame, df_test: pd.DataFrame):
    train_X, train_y = df_train.drop('popular', axis=1), df_train['popular']
    test_X, test_y = df_test.drop('popular', axis=1), df_test['popular']

    tree = DecisionTreeClassifier().fit(train_X, train_y)
    tree_prediction = tree.predict(test_X)
    tree_accuracy = accuracy_score(test_y, tree_prediction)


@JPTest('Aufgabe 3', max_score=2, execute=[imports, init_rnd, load_pickle], prepare_second=True)
async def aufgabe3(left: Notebook, right: Notebook):
    # execute user code and sample solution
    async def result():
        await left.execute_cells('task-3')

        tree = left.ref('tree')
        acc = left.ref('tree_accuracy')

        df_test_y = await left.ref('df_test').drop('popular', axis=1)
        prediction = await tree.predict(df_test_y)

        return await asyncio.gather(
            prediction.receive(),
            acc.receive()
        )

    async def test():
        await right.execute_fun(aufgabe3_solution)

        return await asyncio.gather(
            right.ref('tree_prediction').receive(),
            right.ref('tree_accuracy').receive()
        )

    (result_pred, result_acc), (test_pred, test_acc) = await asyncio.gather(result(), test())

    # compare predictions
    yield np.array_equal(test_pred, result_pred), 1

    # compare accuracy
    yield abs(test_acc - result_acc) < 1e-6, 1


# Aufgabe 4
def aufgabe4_preparation():
    df_new = pd.DataFrame({'budget': [1145774, 14145774],
                           'countries': [1, 2],
                           'runtime': [88, 109],
                           'cast_size': [128, 38],
                           'crew_size': [16, 136],
                           'cast_vote_avg': [4.8, 6.8]})


def aufgabe4_solution(nn, tree, df_new):
    nn_prediction = nn.predict(df_new)
    tree_prediction = tree.predict(df_new)


@JPTestComparison('Aufgabe 4', max_score=2,
                  prepare=[imports, init_rnd, load_pickle,
                           'n_neighbors=5', aufgabe2_solution,
                           aufgabe3_solution,
                           aufgabe4_preparation],
                  execute_left=('task-4',), hold_left=['nn_prediction', 'tree_prediction'],
                  execute_right=aufgabe4_solution, hold_right=['nn_prediction', 'tree_prediction'])
async def aufgabe4(result_nn, result_tree, test_nn, test_tree):
    yield np.array_equal(test_nn, result_nn), 1
    yield np.array_equal(test_tree, result_tree), 1


# Aufgabe 5
def aufgabe5_solution(nn, tree, df_test):
    nn_precision = precision_score(df_test['popular'], nn.predict(df_test.drop('popular', axis=1)))
    nn_recall = recall_score(df_test['popular'], nn.predict(df_test.drop('popular', axis=1)))
    tree_precision = precision_score(df_test['popular'], tree.predict(df_test.drop('popular', axis=1)))
    tree_recall = recall_score(df_test['popular'], tree.predict(df_test.drop('popular', axis=1)))


@JPTestComparison('Aufgabe 5', max_score=2,
                  prepare=[imports, init_rnd, load_pickle,
                           'n_neighbors=5', aufgabe2_solution,
                           aufgabe3_solution],
                  execute_left=('task-5',),
                  hold_left=['nn_precision', 'nn_recall', 'tree_precision', 'tree_recall'],
                  execute_right=aufgabe5_solution,
                  hold_right=['nn_precision', 'nn_recall', 'tree_precision', 'tree_recall'])
async def aufgabe5(nn_p_r, nn_r_r, tree_p_r, tree_r_r, nn_p_t, nn_r_t, tree_p_t, tree_r_t):
    yield abs(nn_p_r - nn_p_t) < 1e-6, 0.5
    yield abs(nn_r_r - nn_r_t) < 1e-6, 0.5
    yield abs(tree_p_r - tree_p_t) < 1e-6, 0.5
    yield abs(tree_r_r - tree_r_t) < 1e-6, 0.5
