# -*- encoding: utf-8 -*-
from abjad import *



def test_sequencetools_flatten_sequence_at_indices_01():
    r'''Works with positive indices.
    '''

    sequence_1 = [0, 1, [2, 3, 4], [5, 6, 7]]
    sequence_2 = sequencetools.flatten_sequence_at_indices(sequence_1, [2])

    assert sequence_2 == [0, 1, 2, 3, 4, [5, 6, 7]]


def test_sequencetools_flatten_sequence_at_indices_02():
    r'''Works with negative indices.
    '''

    sequence_1 = [0, 1, [2, 3, 4], [5, 6, 7]]
    works = sequencetools.flatten_sequence_at_indices(sequence_1, [-1])

    assert works == [0, 1, [2, 3, 4], 5, 6, 7]


def test_sequencetools_flatten_sequence_at_indices_03():
    r'''Boundary cases.
    '''

    sequence_1 = [0, 1, [2, 3, 4], [5, 6, 7]]

    sequence_2 = sequencetools.flatten_sequence_at_indices(sequence_1, [])
    assert sequence_2 == [0, 1, [2, 3, 4], [5, 6, 7]]

    sequence_2 = sequencetools.flatten_sequence_at_indices(sequence_1, [99])
    assert sequence_2 == [0, 1, [2, 3, 4], [5, 6, 7]]

    sequence_2 = sequencetools.flatten_sequence_at_indices(sequence_1, [-99])
    assert sequence_2 == [0, 1, [2, 3, 4], [5, 6, 7]]
