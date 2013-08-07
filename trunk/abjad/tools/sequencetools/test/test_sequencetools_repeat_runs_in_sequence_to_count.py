# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_repeat_runs_in_sequence_to_count_01():

    sequence_1 = range(20)
    sequence_2 = sequencetools.repeat_runs_in_sequence_to_count(sequence_1, [(0, 2, 10)])

    assert sequence_2 == [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_repeat_runs_in_sequence_to_count_02():

    sequence_1 = range(20)
    sequence_2 = sequencetools.repeat_runs_in_sequence_to_count(sequence_1, [(0, 2, 5), (10, 2, 5)])

    assert sequence_2 == [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, (10, 11, 10, 11, 10, 11, 10, 11, 10, 11), 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_repeat_runs_in_sequence_to_count_03():

    sequence_1 = range(20)
    sequence_2 = sequencetools.repeat_runs_in_sequence_to_count(sequence_1, [(18, 4, 2)])

    assert sequence_2 == [0, 1, (18, 19, 0, 1, 18, 19, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_repeat_runs_in_sequence_to_count_04():

    sequence_1 = range(20)
    sequence_2 = sequencetools.repeat_runs_in_sequence_to_count(sequence_1, [(18, 8, 2)])

    assert sequence_2 == [0, 1, 2, 3, 4, 5, (18, 19, 0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 4, 5), 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
