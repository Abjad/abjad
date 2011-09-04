from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_01():

    t = list(sequencetools.remove_sequence_elements_at_indices_cyclically(range(20), [0, 1], 5))
    assert t == [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19]


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_02():

    t = list(sequencetools.remove_sequence_elements_at_indices_cyclically(
        range(20), [0, 1], 5, 1))
    assert t == [0, 3, 4, 5, 8, 9, 10, 13, 14, 15, 18, 19]


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_03():

    t = list(sequencetools.remove_sequence_elements_at_indices_cyclically(range(20), [], 5))
    assert t == range(20)


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_04():

    t = list(sequencetools.remove_sequence_elements_at_indices_cyclically(
        range(20), [-1, 99, 100], 5))
    assert t == range(20)
