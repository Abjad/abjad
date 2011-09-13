from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid_subdivide_indices_01():
    a = QGrid([0, 0], 0)
    b = a.subdivide_indices([(0, 2)])
    assert a == QGrid([0, 0], 0)
    assert b == QGrid([[0, 0], 0], 0)
    c = b.subdivide_indices([(0, 2), (2, 5)])
    assert b == QGrid([[0, 0], 0], 0)
    assert c == QGrid([[[0, 0], 0], [0, 0, 0, 0, 0]], 0)
