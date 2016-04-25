# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.quantizationtools import *


def test_quantizationtools_QGrid_distance_01():

    q_grid = QGrid()

    assert q_grid.distance is None

    a = QEventProxy(SilentQEvent(0,        ['A']), 0)
    q_grid.fit_q_events([a])
    assert q_grid.distance == Offset(0)

    b = QEventProxy(SilentQEvent((1, 20),  ['B']), (1, 20))
    q_grid.fit_q_events([b])
    assert q_grid.distance == Offset(1, 40)

    c = QEventProxy(SilentQEvent((9, 20),  ['C']), (9, 20))
    q_grid.fit_q_events([c])
    assert q_grid.distance == Offset(1, 6)

    d = QEventProxy(SilentQEvent((1, 2),   ['D']), (1, 2))
    q_grid.fit_q_events([d])
    assert q_grid.distance == Offset(1, 4)

    e = QEventProxy(SilentQEvent((11, 20), ['E']), (11, 20))
    q_grid.fit_q_events([e])
    assert q_grid.distance == Offset(29, 100)

    f = QEventProxy(SilentQEvent((19, 20), ['F']), (19, 20))
    q_grid.fit_q_events([f])
    assert q_grid.distance == Offset(1, 4)

    g = QEventProxy(SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([g])
    assert q_grid.distance == Offset(3, 14)

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == Offset(1, 35)
