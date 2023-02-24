from typing import List

from jptest2 import *


def imports():
    import re


# Aufgabe 1
def aufgabe1_solution():
    with open('faust.txt') as file:
        text = file.read()


@JPTestComparison('Aufgabe 1', max_score=1,
                  execute_left=[imports, ('task-1',)], hold_left='text',
                  execute_right=[imports, aufgabe1_solution], hold_right='text')
async def aufgabe1(result: str, test: str):
    yield result == test, 1


# Aufgabe 2
def aufgabe2_1_solution(text: str):
    count_er = text.count('er')


def aufgabe2_2_solution(text: str):
    import re
    count_er = sum((1 for _ in re.finditer(r'er', text, re.IGNORECASE)))


@JPTestComparison('Aufgabe 2', max_score=1,
                  execute_left=[imports, aufgabe1_solution, ('task-2-1',)], hold_left='count_er',
                  execute_right=[imports, aufgabe1_solution, aufgabe2_1_solution], hold_right='count_er')
async def aufgabe2_1(result: int, test: int):
    yield result == test, 1, 'Anzahl mit Beachtung der Groß- und Kleinschreibung inkorrekt'


@JPTestComparison('Aufgabe 2', max_score=1,
                  execute_left=[imports, aufgabe1_solution, ('task-2-2',)], hold_left='count_er',
                  execute_right=[imports, aufgabe1_solution, aufgabe2_2_solution], hold_right='count_er')
async def aufgabe2_2(result: int, test: int):
    yield result == test, 1, 'Anzahl ohne Beachtung der Groß- und Kleinschreibung inkorrekt'


# Aufgabe 3
def aufgabe3_solution(text: str):
    import re
    no104 = re.split(r'\n\n+', text)[104]


@JPTestComparison('Aufgabe 3', max_score=1,
                  execute_left=[imports, aufgabe1_solution, ('task-3',)], hold_left='no104',
                  execute_right=[imports, aufgabe1_solution, aufgabe3_solution], hold_right='no104')
async def aufgabe3(result: int, test: int):
    yield result == test, 1, 'Absatz stimmt nicht überein'


# Aufgabe 4
def aufgabe4_solution(text: str):
    import re
    words = re.findall(
        r'[A-Za-z]*a[A-Za-z]*?e[A-Za-z]*?i[A-Za-z]*|'
        r'[A-Za-z]*e[A-Za-z]*?i[A-Za-z]*?o[A-Za-z]*|'
        r'[A-Za-z]*i[A-Za-z]*?o[A-Za-z]*?u[A-Za-z]*',
        text
    )


@JPTestComparison('Aufgabe 4', max_score=2,
                  execute_left=[imports, aufgabe1_solution, ('task-4',)], hold_left='words',
                  execute_right=[imports, aufgabe1_solution, aufgabe4_solution], hold_right='words')
async def aufgabe4(result: List[str], test: List[str]):
    yield len(result) == len(test), 1, 'Länge des Ergebnisses stimmt nicht'
    yield result == test, 1, 'Absatz stimmt nicht überein'
