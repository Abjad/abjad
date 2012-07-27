from abjad.tools.durationtools import Offset
from experimental.quantizationtools import *


def test_QGrid_distance_01():

    q_grid = QGrid()

    assert q_grid.distance is None

    a = ProxyQEvent(SilentQEvent(0,        ['A']), 0)
    q_grid.fit_q_events([a])
    assert q_grid.distance == Offset(0)

    b = ProxyQEvent(SilentQEvent((1, 20),  ['B']), (1, 20))
    q_grid.fit_q_events([b])
    assert q_grid.distance == Offset(1, 40)

    c = ProxyQEvent(SilentQEvent((9, 20),  ['C']), (9, 20))
    q_grid.fit_q_events([c])
    assert q_grid.distance == Offset(1, 6)

    d = ProxyQEvent(SilentQEvent((1, 2),   ['D']), (1, 2))
    q_grid.fit_q_events([d])
    assert q_grid.distance == Offset(1, 4)

    e = ProxyQEvent(SilentQEvent((11, 20), ['E']), (11, 20))
    q_grid.fit_q_events([e])
    assert q_grid.distance == Offset(29, 100)

    f = ProxyQEvent(SilentQEvent((19, 20), ['F']), (19, 20))
    q_grid.fit_q_events([f])
    assert q_grid.distance == Offset(1, 4)

    g = ProxyQEvent(SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([g])
    assert q_grid.distance == Offset(3, 14)

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == Offset(1, 35)
