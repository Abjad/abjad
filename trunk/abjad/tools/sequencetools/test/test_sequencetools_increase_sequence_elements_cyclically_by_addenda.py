from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_increase_sequence_elements_cyclically_by_addenda_01():
    l = range(10)
    t = sequencetools.increase_sequence_elements_cyclically_by_addenda(l, [2, 0])
    assert t == [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]


def test_sequencetools_increase_sequence_elements_cyclically_by_addenda_02():
    l = range(10)
    t = sequencetools.increase_sequence_elements_cyclically_by_addenda(l, [10, -10])
    assert t == [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]


def test_sequencetools_increase_sequence_elements_cyclically_by_addenda_03():
    l = range(10)
    t = sequencetools.increase_sequence_elements_cyclically_by_addenda(l, [10, -10], shield = False)
    assert t == [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]
