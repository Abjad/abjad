from experimental.quantizationtools import *


def test_QGrid_subdivide_leaf_01():

    q_grid = QGrid()

    a = QEventProxy(PitchedQEvent(0, [0]), 0)
    b = QEventProxy(PitchedQEvent((9, 20), [1]), (9, 20))
    c = QEventProxy(PitchedQEvent((1, 2), [2]), (1, 2))
    d = QEventProxy(PitchedQEvent((11, 20), [3]), (11, 20))
    e = QEventProxy(PitchedQEvent(1, [4]), 1)

    q_grid.leaves[0].q_events.extend([a, b, c, d])
    q_grid.leaves[1].q_events.append(e)

    result = q_grid.subdivide_leaf(q_grid.leaves[0], (2, 3))

    assert result == [a, b, c, d]
    assert q_grid.root_node[0] == QGridContainer(
        children=(
            QGridLeaf(duration=2, q_events=[]),
            QGridLeaf(duration=3, q_events=[]),
        ),
        duration=1
        )
