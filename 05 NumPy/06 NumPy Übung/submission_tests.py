import csv
import gzip
import os
import pickle

import numpy as np
from jptest2 import *


@JPSetup
async def convert_dataset():
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


@JPTeardown
async def remove_dataset():
    for filename in '_cast.csv.bz2.pickle.gz', '_cast_names.csv.pickle.gz':
        if os.path.exists(filename):
            os.remove(filename)


# Imports and Loading
# noinspection PyUnresolvedReferences
def imports():
    import numpy as np
    import csv
    import gzip
    import pickle


def load_dataset():
    with gzip.open('_cast.csv.bz2.pickle.gz', 'rb') as file:
        cast = pickle.load(file)

    with gzip.open('_cast_names.csv.pickle.gz', 'rb') as file:
        cast_names = pickle.load(file)


# Aufgabe 1
@JPTestComparison('Aufgabe 1', max_score=2, prepare=imports,
                  execute_left=('task-1',), hold_left=['cast', 'cast_names'],
                  execute_right=load_dataset, hold_right=['cast', 'cast_names'])
async def aufgabe1(result_cast, result_cast_names, test_cast, test_cast_names):
    yield np.array_equal(test_cast, result_cast), 1, 'cast nicht korrekt'
    yield np.array_equal(test_cast_names, result_cast_names), 1, 'cast_names nicht korrekt'


# Aufgabe 2
@JPTestGet('Aufgabe 2', max_score=3,
           execute=[imports, load_dataset, ('task-2',)],
           get=['max_value', 'max_indices', 'names'])
async def aufgabe2(max_value, max_indices, names):
    yield max_value == 57., 0.5, 'max_value nicht korrekt'

    yield (
                  np.array_equal(max_indices, np.array([[1192, 1192], [1677, 1677]]))
                  or (
                          np.array_equal(max_indices[0], np.array([1192, 1677]))
                          and np.array_equal(max_indices[1], np.array([1192, 1677]))
                  )
          ), 1.5, 'max_indices nicht korrekt'

    yield len(names) == 2 and 'Frank Welker' in names and 'Jim Cummings' in names, 1, 'names nicht korrekt'


# Aufgabe 3
def aufgabe3_solution(cast: np.array):
    cast_wo_self = cast * (1 - np.eye(*cast.shape))


@JPTestComparison('Aufgabe 3', max_score=3,
                  prepare=[imports, load_dataset],
                  execute_left=('task-3',), hold_left=['cast_wo_self', 'max_value', 'max_indices', 'names'],
                  execute_right=aufgabe3_solution, hold_right='cast_wo_self')
async def aufgabe3(l_cast_wo_self, l_max_value, l_max_indices, l_names, r_cast_wo_self):
    yield np.array_equal(l_cast_wo_self, r_cast_wo_self), 1, 'cast_wo_self nicht korrekt'

    yield abs(l_max_value - 26) < 1e-6, 0.5, 'max_value nicht korrekt'

    yield (
            np.array_equal(l_max_indices, np.array([[2510, 3204], [3204, 2510]]))
            or (
                    np.array_equal(l_max_indices[0], np.array([2510, 3204]))
                    and np.array_equal(l_max_indices[1], np.array([3204, 2510]))
            )
    ), 1, 'max_indices nicht korrekt'

    yield len(l_names) == 2 and 'Mickie McGowan' in l_names and 'Sherry Lynn' in l_names, 0.5, 'names nicht korrekt'
