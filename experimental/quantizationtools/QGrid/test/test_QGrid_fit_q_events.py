from experimental.quantizationtools import *


def test_QGrid_fit_q_events_01():

    q_grid = QGrid()

    a = ProxyQEvent(SilentQEvent(0,        ['A']), 0)
    b = ProxyQEvent(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = ProxyQEvent(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = ProxyQEvent(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = ProxyQEvent(SilentQEvent((11, 20), ['E']), (11, 20))
    f = ProxyQEvent(SilentQEvent((19, 20), ['F']), (19, 20))
    g = ProxyQEvent(SilentQEvent(1,        ['G']), 1)

    q_grid.fit_q_events([a, b, c, d, e, f, g])

    assert q_grid.leaves[0].q_events == [a, b, c, d]
    assert q_grid.leaves[1].q_events == [e, f, g]

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])

    q_grid.fit_q_events(q_events)

    assert q_grid.leaves[0].q_events == [a, b]
    assert q_grid.leaves[1].q_events == [c, d, e]
    assert q_grid.leaves[2].q_events == [g, f]

