# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_01():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices_cyclically(range(20), [0, 1], 5))
    assert sequence_2 == [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19]


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_02():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices_cyclically(
        range(20), [0, 1], 5, 1))
    assert sequence_2 == [0, 3, 4, 5, 8, 9, 10, 13, 14, 15, 18, 19]


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_03():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices_cyclically(range(20), [], 5))
    assert sequence_2 == range(20)


def test_sequencetools_remove_sequence_elements_at_indices_cyclically_04():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices_cyclically(
        range(20), [-1, 99, 100], 5))
    assert sequence_2 == range(20)
