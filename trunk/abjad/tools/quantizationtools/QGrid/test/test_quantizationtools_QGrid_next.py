from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid_next_01():

    q = QGrid([0, [[[1, 2], 3], 4], 5], 6)
    assert q.next == 6
