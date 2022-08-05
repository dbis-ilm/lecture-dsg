from jptest import *


@JPTest('Aufgabe 1', max_score=2, execute=[
    'z1, z2, z3, z4, z5, z6, z7, z8, z9, z10 = 3, 9, 8, 5, 6, 1, 0, 1, 4, -1',
    ('task-1',)
])
def aufgabe1(tb: JPTestBook):
    s = tb.ref('s')
    yield 145 == s, 1, 's nicht korrekt'

    z10_test = tb.ref('z10_test')
    yield z10_test == 2, 1, 'z10_test nicht korrekt'
