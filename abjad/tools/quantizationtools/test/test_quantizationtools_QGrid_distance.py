import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_QGrid_distance_01():

    q_grid = quantizationtools.QGrid()

    assert q_grid.distance is None

    a = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(0,        ['A']), 0)
    q_grid.fit_q_events([a])
    assert q_grid.distance == abjad.Offset(0)

    b = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 20),  ['B']), (1, 20))
    q_grid.fit_q_events([b])
    assert q_grid.distance == abjad.Offset(1, 40)

    c = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((9, 20),  ['C']), (9, 20))
    q_grid.fit_q_events([c])
    assert q_grid.distance == abjad.Offset(1, 6)

    d = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 2),   ['D']), (1, 2))
    q_grid.fit_q_events([d])
    assert q_grid.distance == abjad.Offset(1, 4)

    e = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((11, 20), ['E']), (11, 20))
    q_grid.fit_q_events([e])
    assert q_grid.distance == abjad.Offset(29, 100)

    f = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((19, 20), ['F']), (19, 20))
    q_grid.fit_q_events([f])
    assert q_grid.distance == abjad.Offset(1, 4)

    g = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([g])
    assert q_grid.distance == abjad.Offset(3, 14)

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == abjad.Offset(1, 35)
