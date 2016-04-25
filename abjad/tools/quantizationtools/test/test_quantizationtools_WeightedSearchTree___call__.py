# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_WeightedSearchTree___call___01():
    definition = {
        'divisors': (2, 3, 5, 7),
        'max_depth': 3,
        'max_divisions': 2,
        }
    search_tree = quantizationtools.WeightedSearchTree(definition)
    q_grid = quantizationtools.QGrid()
    a = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(0,      ['A'], index=1), 0, 1)
    b = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 5), ['B'], index=2), 0, 1)
    c = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 4), ['C'], index=3), 0, 1)
    d = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 3), ['D'], index=4), 0, 1)
    e = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((2, 5), ['E'], index=5), 0, 1)
    f = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 2), ['F'], index=6), 0, 1)
    g = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((3, 5), ['G'], index=7), 0, 1)
    h = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((2, 3), ['H'], index=8), 0, 1)
    i = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((3, 4), ['I'], index=9), 0, 1)
    j = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((4, 5), ['J'], index=10), 0, 1)
    k = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1,      ['K'], index=11), 0, 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])
    q_grids = search_tree(q_grid)

    assert [q_grid.root_node.rtm_format for q_grid in q_grids] == [
        '(1 (1 1))',
        '(1 (2 1))',
        '(1 (1 2))',
        '(1 (4 1))',
        '(1 (3 2))',
        '(1 (2 3))',
        '(1 (1 4))',
        '(1 (6 1))',
        '(1 (5 2))',
        '(1 (4 3))',
        '(1 (3 4))',
        '(1 (2 5))',
        '(1 (1 6))'
    ]
