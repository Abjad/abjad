from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_repeat_runs_in_sequence_to_count_01():

    l = range(20)
    t = sequencetools.repeat_runs_in_sequence_to_count(l, [(0, 2, 10)])

    assert t == [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_repeat_runs_in_sequence_to_count_02():

    l = range(20)
    t = sequencetools.repeat_runs_in_sequence_to_count(l, [(0, 2, 5), (10, 2, 5)])

    assert t == [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, (10, 11, 10, 11, 10, 11, 10, 11, 10, 11), 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_repeat_runs_in_sequence_to_count_03():

    l = range(20)
    t = sequencetools.repeat_runs_in_sequence_to_count(l, [(18, 4, 2)])

    assert t == [0, 1, (18, 19, 0, 1, 18, 19, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


def test_sequencetools_repeat_runs_in_sequence_to_count_04():

    l = range(20)
    t = sequencetools.repeat_runs_in_sequence_to_count(l, [(18, 8, 2)])

    assert t == [0, 1, 2, 3, 4, 5, (18, 19, 0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 4, 5), 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
