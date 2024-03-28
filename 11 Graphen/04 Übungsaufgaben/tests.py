from typing import List

import networkx as nx
from checkmarkandcross import image


def aufgabe1(G: nx.Graph):
    return image(
        isinstance(G, nx.Graph)
        and 'Thor: Ragnarok' in G.nodes
        and 'A Ring of Endless Light' in G.nodes
        and ('Spider-Man and His Amazing Friends', 'Captain America: Civil War') in G.edges
        and ('Alvin and the Chipmunks: Chipwrecked', 'Percy Jackson & the Olympians: The Lightning Thief')
    )


def aufgabe2_1(density: float):
    return image(
        isinstance(density, (float, int))
        and 0 < density < 0.05
    )


def aufgabe2_2(cc: bool):
    return image(
        cc is False
    )


def aufgabe2_3(shortest_path: List[str]):
    return image(
        isinstance(shortest_path, list)
        and len(shortest_path) == 3
        and shortest_path[0] == 'Mickey Mouse'
        and shortest_path[2] == 'Star Wars: Episode III - Revenge of the Sith'
    )


def aufgabe2_4(mdn: str):
    return image(
        isinstance(mdn, str)
        and mdn == 'The Pixar Story'
    )


def aufgabe2_5(mpn: str):
    return image(
        isinstance(mpn, str)
        and mpn == 'The Pixar Story'
    )


def aufgabe2_6(max_clique: List[str]):
    return image(
        isinstance(max_clique, list)
        and len(max_clique) == 56
        and 'The Hunchback of Notre Dame' in max_clique
        and 'Brother Bear 2' in max_clique
        and 'Darkwing Duck' in max_clique
    )
