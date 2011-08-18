from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid___len___01():

    assert len(QGrid([0], 0)) == 2
    assert len(QGrid([0, 0], 0)) == 3
    assert len(QGrid([[0, 0], 0], 0)) == 4
    assert len(QGrid([0, [0, [0, 0]]], 0)) == 5
