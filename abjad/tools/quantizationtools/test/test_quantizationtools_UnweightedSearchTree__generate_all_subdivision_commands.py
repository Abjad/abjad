# -*- coding: utf-8 -*-
import copy
from abjad import *

def test_quantizationtools_UnweightedSearchTree__generate_all_subdivision_commands_01():

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

    commands = search_tree._generate_all_subdivision_commands(q_grid)
    assert commands == (
        ((0, (1, 1)),),
        ((0, (1, 1, 1, 1, 1)),)
        )

    new_q_grid = copy.copy(q_grid)
    q_event_proxies = new_q_grid.subdivide_leaves(commands[0])
    new_q_grid.fit_q_events(q_event_proxies)
    new_q_grid.sort_q_events_by_index()
    new_commands = search_tree._generate_all_subdivision_commands(new_q_grid)

    assert new_q_grid.leaves[0].q_event_proxies == [a, b, c]
    assert new_q_grid.leaves[1].q_event_proxies == [d, e, f, g, h, i]
    assert new_q_grid.leaves[2].q_event_proxies == [j, k]
    assert new_commands == (
        ((0, (1, 1)), (1, (1, 1))),
        ((0, (1, 1)), (1, (1, 1, 1))),
        ((0, (1, 1, 1)), (1, (1, 1))),
        ((0, (1, 1, 1)), (1, (1, 1, 1)))
        )

    new_q_grid = copy.copy(q_grid)
    q_event_proxies = new_q_grid.subdivide_leaves(commands[1])
    new_q_grid.fit_q_events(q_event_proxies)
    new_q_grid.sort_q_events_by_index()
    new_commands = search_tree._generate_all_subdivision_commands(new_q_grid)

    assert new_q_grid.leaves[0].q_event_proxies == [a]
    assert new_q_grid.leaves[1].q_event_proxies == [b, c]
    assert new_q_grid.leaves[2].q_event_proxies == [d, e, f]
    assert new_q_grid.leaves[3].q_event_proxies == [g, h]
    assert new_q_grid.leaves[4].q_event_proxies == [i, j]
    assert new_q_grid.leaves[5].q_event_proxies == [k]
    assert new_commands == ()
