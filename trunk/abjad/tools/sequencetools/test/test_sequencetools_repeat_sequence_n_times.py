from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_repeat_sequence_n_times_01():
    '''Repeat sequence 3 times.
    '''

    t = sequencetools.repeat_sequence_n_times(range(1, 6), 3)
    assert t == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]


def test_sequencetools_repeat_sequence_n_times_02():
    '''Repeat sequence no times.
    '''

    t = sequencetools.repeat_sequence_n_times(range(1, 6), 0)
    assert t == []
