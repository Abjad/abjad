from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid___iter___01():

    q = QGrid([0, [[[1, 2], 3], 4], 5], 6)

    for i, x in enumerate(q):
        assert i == x
