import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_QGrid_subdivide_leaves_01():

    q_grid = quantizationtools.QGrid()

    a = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(0,        ['A']), 0)
    b = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 20),  ['B']), (1, 20))
    c = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((9, 20),  ['C']), (9, 20))
    d = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 2),   ['D']), (1, 2))
    e = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((11, 20), ['E']), (11, 20))
    f = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((19, 20), ['F']), (19, 20))
    g = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1,        ['G']), 1)

    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.extend([e, f, g])

    assert q_grid.root_node.rtm_format == '1'

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])

    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == '(1 (1 1))'

    q_grid.leaves[0].q_event_proxies.extend([a, b])
    q_grid.leaves[1].q_event_proxies.extend([c, d, e])
    q_grid.leaves[2].q_event_proxies.append(f)

    q_events = q_grid.subdivide_leaves([(0, (1, 1)), (1, (1, 1))])

    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == '(1 ((1 (1 1)) (1 (1 1))))'


def test_quantizationtools_QGrid_subdivide_leaves_02():

    q_grid = quantizationtools.QGrid()

    a = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(0,        ['A']), 0)
    b = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 20),  ['B']), (1, 20))
    c = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((9, 20),  ['C']), (9, 20))
    d = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 2),   ['D']), (1, 2))
    e = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((11, 20), ['E']), (11, 20))
    f = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((19, 20), ['F']), (19, 20))
    g = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1,        ['G']), 1)

    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.extend([e, f, g])

    assert q_grid.root_node.rtm_format == '1'

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])

    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == '(1 (1 1))'

    q_grid.leaves[0].q_event_proxies.extend([a, b])
    q_grid.leaves[1].q_event_proxies.extend([c, d, e])
    q_grid.leaves[2].q_event_proxies.append(f)

    q_events = q_grid.subdivide_leaves([(0, (3, 4, 5))])

    assert q_events == [a, b, c]
    assert q_grid.root_node.rtm_format == '(1 ((1 (3 4 5)) 1))'
