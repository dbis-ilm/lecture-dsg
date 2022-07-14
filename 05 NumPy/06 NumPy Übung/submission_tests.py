import csv
import gzip
import os
import pickle

import numpy as np
from jptest import *


@JPPreRun
def convert_dataset():
    # cast
    cast = np.loadtxt('cast.csv.bz2')

    with gzip.open('_cast.csv.bz2.pickle.gz', 'wb', compresslevel=1) as file:
        pickle.dump(cast, file)

    # cast_names
    cast_names = []

    with open('cast_names.csv') as file:
        reader = csv.reader(file)
        for line_number, (_, name) in enumerate(reader):
            if line_number > 0:
                cast_names.append(name)

    with gzip.open('_cast_names.csv.pickle.gz', 'wb', compresslevel=1) as file:
        pickle.dump(cast_names, file)


@JPPostRun
def remove_dataset():
    for filename in '_cast.csv.bz2.pickle.gz', '_cast_names.csv.pickle.gz':
        if os.path.exists(filename):
            os.remove(filename)


# Imports and Loading
imports = '''
    import numpy as np
    import csv
    import gzip
    import pickle
'''

load_dataset = '''
    with gzip.open('_cast.csv.bz2.pickle.gz', 'rb', compresslevel=1) as file:
        cast = pickle.load(file)
        
    with gzip.open('_cast_names.csv.pickle.gz', 'rb', compresslevel=1) as file:
        cast_names = pickle.load(file)
'''


# Aufgabe 1
@JPTest('Aufgabe 1', max_score=2, execute=[imports, ('task-1',)])
def aufgabe1(tb: JPTestBook):
    result_cast, result_cast_names = tb.get('cast', 'cast_names')
    test_cast, test_cast_names = tb.inject(load_dataset, 'cast', 'cast_names')

    yield tb.ref('np').array_equal(test_cast, result_cast), 1, 'cast nicht korrekt'
    yield tb.ref('np').array_equal(test_cast_names, result_cast_names), 1, 'cast_names nicht korrekt'


# Aufgabe 2
@JPTest('Aufgabe 2', max_score=3, execute=[imports, load_dataset, ('task-2',)])
def aufgabe2(tb: JPTestBook):
    result = tb.ref('max_value')
    yield result == 57., 0.5, 'max_value nicht korrekt'

    test1, test2 = tb.inject('''
        max_indices_1 = np.array_equal(max_indices, np.array([[1192, 1192], [1677, 1677]]))
        max_indices_2 = np.array_equal(max_indices[0], np.array([1192, 1677])) \
                    and np.array_equal(max_indices[1], np.array([1192, 1677]))
    ''', 'max_indices_1', 'max_indices_2')
    yield test1 or test2, 1.5, 'max_indices nicht korrekt'

    result = tb.get('names')
    yield len(result) == 2 and 'Frank Welker' in result and 'Jim Cummings' in result, 1, \
          'names nicht korrekt'


# Aufgabe 3
@JPTest('Aufgabe 3', max_score=3, execute=[imports, load_dataset, ('task-3',)])
def aufgabe3(tb: JPTestBook):
    result = tb.get('cast_wo_self')
    test = tb.inject('cast_wo_self = cast * (1 - np.eye(*cast.shape))', 'cast_wo_self')
    yield tb.ref('np').array_equal(test, result), 1, 'cast_wo_self nicht korrekt'

    result = tb.get('max_value')
    yield result == 26., 0.5, 'max_value nicht korrekt'

    test1, test2 = tb.inject('''
        max_indices_1 = np.array_equal(max_indices, np.array([[2510, 3204], [3204, 2510]]))
        max_indices_2 = np.array_equal(max_indices[0], np.array([2510, 3204])) \
                    and np.array_equal(max_indices[1], np.array([3204, 2510]))
    ''', 'max_indices_1', 'max_indices_2')
    yield test1 or test2, 1, 'max_indices nicht korrekt'

    result = tb.get('names')
    yield len(result) == 2 and 'Mickie McGowan' in result and 'Sherry Lynn' in result, 0.5, \
          'names nicht korrekt'
