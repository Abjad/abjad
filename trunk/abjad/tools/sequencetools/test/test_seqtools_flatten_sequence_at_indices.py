from abjad import *
from abjad.tools import sequencetools



def test_sequencetools_flatten_sequence_at_indices_01():
    '''Works with positive indices.'''

    l = [0, 1, [2, 3, 4], [5, 6, 7]]
    t = sequencetools.flatten_sequence_at_indices(l, [2])

    assert t == [0, 1, 2, 3, 4, [5, 6, 7]]


def test_sequencetools_flatten_sequence_at_indices_02():
    '''Works with negative indices.'''

    l = [0, 1, [2, 3, 4], [5, 6, 7]]
    t = sequencetools.flatten_sequence_at_indices(l, [-1])

    assert t == [0, 1, [2, 3, 4], 5, 6, 7]


def test_sequencetools_flatten_sequence_at_indices_03():
    '''Boundary cases.'''

    l = [0, 1, [2, 3, 4], [5, 6, 7]]

    t = sequencetools.flatten_sequence_at_indices(l, [])
    assert t == [0, 1, [2, 3, 4], [5, 6, 7]]

    t = sequencetools.flatten_sequence_at_indices(l, [99])
    assert t == [0, 1, [2, 3, 4], [5, 6, 7]]

    t = sequencetools.flatten_sequence_at_indices(l, [-99])
    assert t == [0, 1, [2, 3, 4], [5, 6, 7]]
