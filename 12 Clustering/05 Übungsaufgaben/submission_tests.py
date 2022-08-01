import os

import pandas as pd
from jptest import *

# Vorbereitungen
imports = '''
    import numpy.random
    
    import pandas as pd
    import plotly.express as px
    
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.preprocessing import MinMaxScaler
'''
load_data = 'df = pd.read_pickle("df.pickle")'
init_rnd = 'numpy.random.seed(16)'


@JPPreRun
def pre():
    # read data
    df: pd.DataFrame = pd.read_csv('clustering.csv')

    mva_min, mva_max = df['movie_vote_average'].min(), df['movie_vote_average'].max()
    df['movie_vote_average'] = (df['movie_vote_average'] - mva_min) / (mva_max - mva_min)

    # shuffle movie_vote_average column
    df['movie_vote_average'] = df['movie_vote_average'].sample(frac=1, random_state=312).reset_index(drop=True)

    # store pickled
    df.to_pickle('df.pickle')


@JPPostRun
def post():
    if os.path.exists('df.pickle'):
        os.remove('df.pickle')


# Aufgabe 1
@JPTest('Aufgabe 1', max_score=2, execute=[imports, {
    'execute': ('task-1',),
    'track': {
        'px.scatter': [('x', 1), ('y', 2)]
    }
}])
def aufgabe1(tb: JPTestBook, params: JPTestParams):
    df_result = tb.get('df')
    df_test = tb.inject('''
        df = pd.read_csv('clustering.csv')
        
        mva_min, mva_max = df['movie_vote_average'].min(), df['movie_vote_average'].max()
        df['movie_vote_average'] = (df['movie_vote_average'] - mva_min) / (mva_max - mva_min)
    ''', 'df')

    yield df_test.equals(df_result), 1

    p = params.last_value('x'), params.last_value('y')
    yield p == ('adult_ratio', 'movie_vote_average') or p == ('movie_vote_average', 'adult_ratio'), 1


# Aufgabe 2
@JPTest('Aufgabe 2', max_score=2, execute=[imports, load_data, init_rnd, {
    'execute': ('task-2',),
    'track': {
        'KMeans': ('n_clusters', 0)
    },
}])
def aufgabe2(tb: JPTestBook, params: JPTestParams):
    result = tb.get('df')

    tb.inject(imports)
    tb.inject(load_data)
    tb.inject(init_rnd)

    n_clusters = params.last_value('n_clusters')
    test = tb.inject(f'''
        df['kmeans'] = KMeans({n_clusters}).fit_predict(df[['adult_ratio', 'movie_vote_average']])
    ''', 'df')

    yield test.equals(result), 2


# Aufgabe 3
@JPTest('Aufgabe 3', max_score=2, execute=[imports, load_data, init_rnd, {
    'execute': ('task-3',),
    'track': {
        'DBSCAN': [
            ('eps', 0),
            ('min_samples', 1)
        ]
    },
}])
def aufgabe3(tb: JPTestBook, params: JPTestParams):
    result = tb.get('df')

    tb.inject(imports)
    tb.inject(load_data)
    tb.inject(init_rnd)

    e, ms = params.last_value('eps'), params.last_value('min_samples')
    test = tb.inject(f'''
        df['dbscan'] = DBSCAN(eps={e}, min_samples={ms}).fit_predict(df[['adult_ratio', 'movie_vote_average']])
    ''', 'df')

    yield test.equals(result), 2
