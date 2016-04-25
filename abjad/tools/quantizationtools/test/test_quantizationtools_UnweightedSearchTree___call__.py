# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_UnweightedSearchTree___call___01():

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

    assert q_grids[0].root_node.rtm_format == '(1 (1 1))'
    assert q_grids[1].root_node.rtm_format == '(1 (1 1 1 1 1))'
