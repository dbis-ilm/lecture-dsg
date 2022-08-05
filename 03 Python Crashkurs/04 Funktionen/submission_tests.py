from jptest import *


def reference(x):
    y = 0

    while x > 0:
        y += x % 10
        x = x // 10

    return y