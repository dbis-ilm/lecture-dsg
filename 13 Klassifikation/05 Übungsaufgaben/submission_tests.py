import os

import pandas as pd
from jptest import *
from sklearn.preprocessing import StandardScaler

# Vorbereitungen
imports = '''
    import pandas as pd
    
    import numpy as np
    import random
    
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score, precision_score, recall_score
'''
load_data = '''
    df = pd.read_pickle("df.pickle")
    df_train, df_test = train_test_split(df, test_size=0.25)
'''
init_rnd = '''
    np.random.seed(14884)
    random.seed(14885)
'''


@JPPreRun
def pre():
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
def post():
    if os.path.exists('df.pickle'):
        os.remove('df.pickle')


# Aufgabe 1
@JPTest('Aufgabe 1', max_score=2, execute=[imports, init_rnd, load_data, ('task-1',)])
def aufgabe1(tb: JPTestBook):
    df_result, df_train_result, df_test_result = tb.get('df', 'df_train', 'df_test')

    tb.inject(init_rnd)
    tb.inject(load_data)
    df_test, df_train_test, df_test_test = tb.inject('''
        df = pd.read_csv('classification_movies.csv')
        df_train, df_test = train_test_split(df, test_size=0.25)
    ''', 'df', 'df_train', 'df_test')

    yield df_test.equals(df_test), 1
    yield df_train_test.equals(df_train_result), 0.5
    yield df_test_test.equals(df_test_result), 0.5


# Aufgabe 2
solution2 = '''
    X, y = df_train.drop('popular', axis=1), df_train['popular']
    nn = KNeighborsClassifier(n_neighbors=%d).fit(X, y)
    nn_accuracy = accuracy_score(df_test['popular'], nn.predict(df_test.drop('popular', axis=1)))
'''


@JPTest('Aufgabe 2', max_score=2, execute=[imports, init_rnd, load_data, ('task-2',)])
def aufgabe2(tb: JPTestBook):
    nn_result, nn_acc_result = tb.get('nn', 'nn_accuracy')
    n_neighbors = tb.inject('n_neighbors = int(nn.n_neighbors)', 'n_neighbors')

    tb.inject(init_rnd)
    tb.inject(load_data)

    nn_test, nn_acc_test = tb.inject(solution2 % n_neighbors, 'nn', 'nn_accuracy')

    # Vorhersagen vergleichen
    df_test = tb.ref('df_test').drop('popular', axis=1)

    pred_result = nn_result.predict(df_test)
    pred_test = nn_test.predict(df_test)

    yield tb.ref('np').array_equal(pred_test, pred_result), 1

    # Accuracy vergleichen
    yield abs(nn_acc_test - nn_acc_result) < 1e-6, 1


# Aufgabe 3
solution3 = '''
    X, y = df_train.drop('popular', axis=1), df_train['popular']
    tree = DecisionTreeClassifier().fit(X, y)
    tree_accuracy = accuracy_score(df_test['popular'], tree.predict(df_test.drop('popular', axis=1)))
'''


@JPTest('Aufgabe 3', max_score=2, execute=[imports, init_rnd, load_data, ('task-3',)])
def aufgabe3(tb: JPTestBook):
    tree_result, tree_acc_result = tb.get('tree', 'tree_accuracy')

    tb.inject(init_rnd)
    tb.inject(load_data)

    tree_test, tree_acc_test = tb.inject(solution3, 'tree', 'tree_accuracy')

    # Vorhersagen vergleichen
    df_test = tb.ref('df_test').drop('popular', axis=1)

    pred_result = tree_result.predict(df_test)
    pred_test = tree_test.predict(df_test)

    yield tb.ref('np').array_equal(pred_test, pred_result), 1

    # Accuracy vergleichen
    yield abs(tree_acc_test - tree_acc_result) < 1e-6, 1


# Aufgabe 4
define_new = '''
    df_new = pd.DataFrame({'budget': [1145774, 14145774],
                           'countries': [1, 2],
                           'runtime': [88, 109],
                           'cast_size': [128, 38],
                           'crew_size': [16, 136],
                           'cast_vote_avg': [4.8, 6.8]})
'''


@JPTest('Aufgabe 4', max_score=2, execute=[imports, init_rnd, load_data,
                                           solution2 % 5, solution3,
                                           define_new, ('task-4',)])
def aufgabe4(tb: JPTestBook):
    nn_result, tree_result = tb.get('nn_prediction', 'tree_prediction')

    tb.execute([imports, init_rnd, load_data, solution2 % 5, solution3, define_new])
    nn_test, tree_test = tb.inject('''
        nn_prediction = nn.predict(df_new)
        tree_prediction = tree.predict(df_new)
    ''', 'nn_prediction', 'tree_prediction')

    yield tb.ref('np').array_equal(nn_test, nn_result), 1
    yield tb.ref('np').array_equal(tree_test, tree_result), 1


# Aufgabe 5
@JPTest('Aufgabe 5', max_score=2, execute=[imports, init_rnd, load_data, solution2 % 5, solution3, ('task-5',)])
def aufgabe5(tb: JPTestBook):
    nn_p_r, nn_r_r, tree_p_r, tree_r_r = tb.get('nn_precision', 'nn_recall', 'tree_precision', 'tree_recall')

    tb.execute([imports, init_rnd, load_data, solution2 % 5, solution3])
    nn_p_t, nn_r_t, tree_p_t, tree_r_t = tb.inject('''
        nn_precision = precision_score(df_test['popular'], nn.predict(df_test.drop('popular', axis=1)))
        nn_recall = recall_score(df_test['popular'], nn.predict(df_test.drop('popular', axis=1)))
        tree_precision = precision_score(df_test['popular'], tree.predict(df_test.drop('popular', axis=1)))
        tree_recall = recall_score(df_test['popular'], tree.predict(df_test.drop('popular', axis=1)))
    ''', 'nn_precision', 'nn_recall', 'tree_precision', 'tree_recall')

    yield abs(nn_p_r - nn_p_t) < 1e-6, 0.5
    yield abs(nn_r_r - nn_r_t) < 1e-6, 0.5
    yield abs(tree_p_r - tree_p_t) < 1e-6, 0.5
    yield abs(tree_r_r - tree_r_t) < 1e-6, 0.5
