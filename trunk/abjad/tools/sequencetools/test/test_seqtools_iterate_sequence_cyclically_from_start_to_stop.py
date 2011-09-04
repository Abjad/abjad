from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_iterate_sequence_cyclically_from_start_to_stop_01():

    l = range(20)
    t = sequencetools.iterate_sequence_cyclically_from_start_to_stop(l, 18, 10)

    assert list(t) == [18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_sequencetools_iterate_sequence_cyclically_from_start_to_stop_02():

    l = range(20)
    t = sequencetools.iterate_sequence_cyclically_from_start_to_stop(l, 10, 18)
    assert list(t) == [10, 11, 12, 13, 14, 15, 16, 17]

    t = sequencetools.iterate_sequence_cyclically_from_start_to_stop(l, 10, 10)
    assert list(t) == []
