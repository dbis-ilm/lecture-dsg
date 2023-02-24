from jptest2 import *


# Aufgabe 1
def to_list(fun, *args):
    return list(fun(*args))


def check_for_generator(fun):
    from types import GeneratorType
    return callable(fun) and isinstance(fun(1024), GeneratorType)


@JPTest('Aufgabe 1', max_score=2, execute=('task-1',))
async def aufgabe1(nb: Notebook):
    cfg = await nb.inject_fun(check_for_generator)
    tl = await nb.inject_fun(to_list)
    even_ref = nb.ref('even')

    isgenerator = await cfg(even_ref).receive()
    yield isgenerator, 1

    result = await tl(even_ref, 15).receive()
    yield result == list(range(0, 15, 2)), 0.5

    result = await tl(even_ref, 1025).receive()
    yield result == list(range(0, 1025, 2)), 0.5


# Aufgabe 2
def solution():
    def even(i):
        return range(1, i, 3)


@JPTest('Aufgabe 2', max_score=1, execute=[solution, ('task-2',)])
async def aufgabe2(nb: Notebook):
    result = await nb.ref('even_list').receive()
    yield result == list(range(1, 256, 3)), 1
