from experimental.quantizationtools import *


def test_QGrid_subdivide_leaves_01():

    q_grid = QGrid()

    a = ProxyQEvent(SilentQEvent(0,        ['A']), 0)
    b = ProxyQEvent(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = ProxyQEvent(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = ProxyQEvent(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = ProxyQEvent(SilentQEvent((11, 20), ['E']), (11, 20))
    f = ProxyQEvent(SilentQEvent((19, 20), ['F']), (19, 20))
    g = ProxyQEvent(SilentQEvent(1,        ['G']), 1)

    q_grid.leaves[0].q_events.extend([a, b, c, d])
    q_grid.leaves[1].q_events.extend([e, f, g])

    assert q_grid.root_node.rtm_format == '(1 (1))'

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])

    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == '(1 ((1 (1 1))))'

    q_grid.leaves[0].q_events.extend([a, b])
    q_grid.leaves[1].q_events.extend([c, d, e])
    q_grid.leaves[2].q_events.append(f)

    q_events = q_grid.subdivide_leaves([(0, (1, 1)), (1, (1, 1))])

    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == '(1 ((1 ((1 (1 1)) (1 (1 1))))))'


def test_QGrid_subdivide_leaves_02():

    q_grid = QGrid()

    a = ProxyQEvent(SilentQEvent(0,        ['A']), 0)
    b = ProxyQEvent(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = ProxyQEvent(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = ProxyQEvent(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = ProxyQEvent(SilentQEvent((11, 20), ['E']), (11, 20))
    f = ProxyQEvent(SilentQEvent((19, 20), ['F']), (19, 20))
    g = ProxyQEvent(SilentQEvent(1,        ['G']), 1)

    q_grid.leaves[0].q_events.extend([a, b, c, d])
    q_grid.leaves[1].q_events.extend([e, f, g])

    assert q_grid.root_node.rtm_format == '(1 (1))'

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])

    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == '(1 ((1 (1 1))))'

    q_grid.leaves[0].q_events.extend([a, b])
    q_grid.leaves[1].q_events.extend([c, d, e])
    q_grid.leaves[2].q_events.append(f)

    q_events = q_grid.subdivide_leaves([(0, (3, 4, 5))])

    assert q_events == [a, b, c]
    assert q_grid.root_node.rtm_format == '(1 ((1 ((1 (3 4 5)) 1))))'
