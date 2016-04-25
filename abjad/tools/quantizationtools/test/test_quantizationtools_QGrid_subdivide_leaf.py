# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.quantizationtools import *


def test_quantizationtools_QGrid_subdivide_leaf_01():

    q_grid = QGrid()

    a = QEventProxy(PitchedQEvent(0, [0]), 0)
    b = QEventProxy(PitchedQEvent((9, 20), [1]), (9, 20))
    c = QEventProxy(PitchedQEvent((1, 2), [2]), (1, 2))
    d = QEventProxy(PitchedQEvent((11, 20), [3]), (11, 20))
    e = QEventProxy(PitchedQEvent(1, [4]), 1)

    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.append(e)

    result = q_grid.subdivide_leaf(q_grid.leaves[0], (2, 3))

    assert result == [a, b, c, d]
    root_node = QGridContainer(
        children=[
            QGridLeaf(preprolated_duration=2, q_event_proxies=[]),
            QGridLeaf(preprolated_duration=3, q_event_proxies=[]),
            ],
        preprolated_duration=1
        )
    assert format(q_grid.root_node) == format(root_node)
