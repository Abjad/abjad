from abjad import *
from abjad.tools import seqtools


def test_seqtools_is_monotonically_increasing_sequence_01( ):
    '''True when the elements in l increase monotonically.'''

    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert seqtools.is_monotonically_increasing_sequence(l)

    l = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
    assert seqtools.is_monotonically_increasing_sequence(l)


def test_seqtools_is_monotonically_increasing_sequence_02( ):
    '''False when the elements in l do not increase monotonically.'''

    l = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert not seqtools.is_monotonically_increasing_sequence(l)

    l = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
    assert not seqtools.is_monotonically_increasing_sequence(l)


def test_seqtools_is_monotonically_increasing_sequence_03( ):
    '''True when l is empty.'''

    l = [ ]
    assert seqtools.is_monotonically_increasing_sequence(l)
