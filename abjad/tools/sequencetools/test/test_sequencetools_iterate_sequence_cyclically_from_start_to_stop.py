# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_iterate_sequence_cyclically_from_start_to_stop_01():

    sequence_1 = range(20)
    sequence_2 = sequencetools.iterate_sequence_cyclically_from_start_to_stop(sequence_1, 18, 10)

    assert list(sequence_2) == [18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_sequencetools_iterate_sequence_cyclically_from_start_to_stop_02():

    sequence_1 = range(20)
    sequence_2 = sequencetools.iterate_sequence_cyclically_from_start_to_stop(sequence_1, 10, 18)
    assert list(sequence_2) == [10, 11, 12, 13, 14, 15, 16, 17]

    sequence_2 = sequencetools.iterate_sequence_cyclically_from_start_to_stop(sequence_1, 10, 10)
    assert list(sequence_2) == []
