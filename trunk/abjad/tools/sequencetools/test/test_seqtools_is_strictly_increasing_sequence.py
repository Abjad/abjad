from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_is_strictly_increasing_sequence_01():
    '''True when the elements in l increase strictly.'''

    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert sequencetools.is_strictly_increasing_sequence(l)


def test_sequencetools_is_strictly_increasing_sequence_02():
    '''False when the elements in l do not increase strictly.'''

    l = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert not sequencetools.is_strictly_increasing_sequence(l)

    l = [3, 3, 3, 3, 3, 3, 3, 2, 1, 0]
    assert not sequencetools.is_strictly_increasing_sequence(l)

    l = [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]
    assert not sequencetools.is_strictly_increasing_sequence(l)


def test_sequencetools_is_strictly_increasing_sequence_03():
    '''True when l is empty.'''

    l = []
    assert sequencetools.is_strictly_increasing_sequence(l)


def test_sequencetools_is_strictly_increasing_sequence_04():
    '''False when expr is not a sequence.'''

    assert not sequencetools.is_strictly_increasing_sequence(17)
