from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid___getitem___01():

    q = QGrid([0, [[[1, 2], 3], 4], 5], 6)
    assert q[0] == 0
    assert q[1] == 1
    assert q[2] == 2
    assert q[3] == 3
    assert q[4] == 4
    assert q[5] == 5
    assert q[6] == 6
