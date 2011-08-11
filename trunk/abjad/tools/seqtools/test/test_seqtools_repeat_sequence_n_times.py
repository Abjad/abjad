from abjad import *
from abjad.tools import seqtools


def test_seqtools_repeat_sequence_n_times_01( ):
    '''Repeat sequence 3 times.
    '''

    t = seqtools.repeat_sequence_n_times(range(1, 6), 3)
    assert t == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]


def test_seqtools_repeat_sequence_n_times_02( ):
    '''Repeat sequence no times.
    '''

    t = seqtools.repeat_sequence_n_times(range(1, 6), 0)
    assert t == [ ]
