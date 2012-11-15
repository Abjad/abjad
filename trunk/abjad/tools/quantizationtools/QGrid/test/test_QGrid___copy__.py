from experimental import quantizationtools
import copy


def test_QGrid___copy___01():

    q_grid = quantizationtools.QGrid()
    copied = copy.copy(q_grid)

    assert q_grid == copied
    assert q_grid is not copied

    assert q_grid.root_node == copied.root_node
    assert q_grid.root_node is not copied.root_node

    assert q_grid.next_downbeat == copied.next_downbeat
    assert q_grid.next_downbeat is not copied.next_downbeat
