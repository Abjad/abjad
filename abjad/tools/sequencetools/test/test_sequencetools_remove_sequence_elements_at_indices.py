# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_remove_sequence_elements_at_indices_01():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices(range(20), [1, 16, 17, 18]))
    assert sequence_2 == [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19]


def test_sequencetools_remove_sequence_elements_at_indices_02():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices([], [1, 2, 3, 4, 5]))
    assert sequence_2 == []


def test_sequencetools_remove_sequence_elements_at_indices_03():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices(range(5), []))
    assert sequence_2 == [0, 1, 2, 3, 4]


def test_sequencetools_remove_sequence_elements_at_indices_04():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices(range(5), [99, 100, 101]))
    assert sequence_2 == [0, 1, 2, 3, 4]


def test_sequencetools_remove_sequence_elements_at_indices_05():

    sequence_2 = list(sequencetools.remove_sequence_elements_at_indices(range(5), [-1, -2, -3]))
    assert sequence_2 == [0, 1, 2, 3, 4]
