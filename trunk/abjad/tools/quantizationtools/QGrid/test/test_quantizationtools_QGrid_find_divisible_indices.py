from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid_find_divisible_indices_01():
    q = QGrid([0, [0, [0, [0, 0]]]], 0)
    assert q.find_divisible_indices([]) == []
    assert q.find_divisible_indices([0]) == []
    assert q.find_divisible_indices([0, 0.5]) == []
    assert q.find_divisible_indices([0.25]) == [0]
    assert q.find_divisible_indices([0.25, 0.8, 0.99]) == [0, 2, 4]
    assert q.find_divisible_indices([1]) == []
    assert q.find_divisible_indices([-0.1, 1.1]) == []
