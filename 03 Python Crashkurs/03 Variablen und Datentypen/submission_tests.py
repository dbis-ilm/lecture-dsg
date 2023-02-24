from jptest2 import *


def create_isbn():
    z1, z2, z3, z4, z5, z6, z7, z8, z9, z10 = 3, 9, 8, 5, 6, 1, 0, 1, 4, -1


@JPTest('Aufgabe 1', max_score=2, execute=[
    create_isbn,
    ('task-1',)
])
async def aufgabe1(nb: Notebook):
    s = await nb.ref('s').receive()
    yield 145 == s, 1, 's nicht korrekt'

    z10_test = await nb.ref('z10_test').receive()
    yield z10_test == 2, 1, 'z10_test nicht korrekt'
