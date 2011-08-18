from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid___eq___01():

    a = QGrid([0, 0], 0)
    b = QGrid([0, 0, 0], 1)
    c = QGrid([0, 0], 1)
    d = QGrid([0, 0], 0)

    assert a != b
    assert a != c
    assert b != c
    assert a == d
