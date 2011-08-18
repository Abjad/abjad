from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid_find_parentage_of_index_01():

    q = QGrid([0, [[0, 0], 0, 0], 0, 0, 0], 0)
    assert q.find_parentage_of_index(0) == (5,)
    assert q.find_parentage_of_index(1) == (5, 3, 2)
    assert q.find_parentage_of_index(2) == (5, 3, 2)
    assert q.find_parentage_of_index(3) == (5, 3)
    assert q.find_parentage_of_index(4) == (5, 3)
    assert q.find_parentage_of_index(5) == (5,)
    assert q.find_parentage_of_index(6) == (5,)
    assert q.find_parentage_of_index(7) == (5,)
    assert q.find_parentage_of_index(8) is None
