from abjad import *
from abjad.tools import seqtools


def test_seqtools_is_strictly_decreasing_sequence_01( ):
    '''True when the elements in l decrease strictly.'''

    l = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert seqtools.is_strictly_decreasing_sequence(l)


def test_seqtools_is_strictly_decreasing_sequence_02( ):
    '''False when the elements in l do not decrease strictly.'''

    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert not seqtools.is_strictly_decreasing_sequence(l)

    l = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
    assert not seqtools.is_strictly_decreasing_sequence(l)

    l = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
    assert not seqtools.is_strictly_decreasing_sequence(l)


def test_seqtools_is_strictly_decreasing_sequence_03( ):
    '''True when l is empty.'''

    l = [ ]
    assert seqtools.is_strictly_decreasing_sequence(l)


def test_seqtools_is_strictly_decreasing_sequence_04( ):
    '''False when expr is not a sequence.'''

    assert not seqtools.is_strictly_decreasing_sequence(17)
