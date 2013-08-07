# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_get_indices_of_sequence_elements_equal_to_true_01():

    sequence_1 = [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
    sequence_2 = sequencetools.get_indices_of_sequence_elements_equal_to_true(sequence_1)
    assert sequence_2 == (3, 4, 5, 9, 10, 11)


def test_sequencetools_get_indices_of_sequence_elements_equal_to_true_02():

    sequence_1 = [0, 0, 0, 0, 0, 0]
    sequence_2 = sequencetools.get_indices_of_sequence_elements_equal_to_true(sequence_1)
    assert sequence_2 == ()
