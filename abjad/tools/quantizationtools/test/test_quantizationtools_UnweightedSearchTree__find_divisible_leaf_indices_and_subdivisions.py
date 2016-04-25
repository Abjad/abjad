# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_UnweightedSearchTree__find_divisible_leaf_indices_and_subdivisions_01():

    definition = {
        2: {
            2: {
                2: None
            },
            3: None
        },
        5: None
    }
    search_tree = quantizationtools.UnweightedSearchTree(definition)

    q_grid = quantizationtools.QGrid()
    a = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(0,      ['A']), 0, 1)
    b = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 5), ['B']), 0, 1)
    c = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 4), ['C']), 0, 1)
    d = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 3), ['D']), 0, 1)
    e = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((2, 5), ['E']), 0, 1)
    f = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 2), ['F']), 0, 1)
    g = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((3, 5), ['G']), 0, 1)
    h = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((2, 3), ['H']), 0, 1)
    i = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((3, 4), ['I']), 0, 1)
    j = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((4, 5), ['J']), 0, 1)
    k = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1,      ['K']), 0, 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])

    indices, subdivisions = search_tree._find_divisible_leaf_indices_and_subdivisions(q_grid)

    assert indices == [0]
    assert subdivisions == [((1, 1), (1, 1, 1, 1, 1))]
