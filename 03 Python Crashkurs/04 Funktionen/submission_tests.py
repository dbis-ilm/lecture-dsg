import random

from jptest2 import *


# Aufgabe 1
def digit_sum(x):
    y = 0

    while x > 0:
        y += x % 10
        x = x // 10

    return y


def call_digit_sum():
    return [digit_sum(i) for i in range(0, 10_000)]


@JPTest('Aufgabe 1', max_score=1, execute=('task-1',))
async def aufgabe1(nb: Notebook):
    cds = await nb.inject_fun(call_digit_sum)

    result = await cds().receive()
    test = call_digit_sum()

    yield test == result, 1


# Aufgabe 2
def info(*args):
    return len(args), min(args), max(args)


def call_info(data):
    return [info(d) for d in data]


@JPTest('Aufgabe 2', max_score=1, execute=('task-2',))
async def aufgabe2(nb: Notebook):
    # create a list of example parameters
    random.seed(196)
    data = [random.sample(range(5000), random.randint(1, 20)) for _ in range(200)]

    # inject `call_info`
    ci = await nb.inject_fun(call_info)

    # run in notebook and locally
    result = await ci(data).receive()
    test = call_info(data)

    # compare result
    yield test == result, 1
