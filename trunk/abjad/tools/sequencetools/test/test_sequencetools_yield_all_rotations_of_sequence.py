from abjad import *
import py.test


def test_sequencetools_yield_all_rotations_of_sequence_01():
    '''Yield all rotations of list.
    '''

    rotations = list(sequencetools.yield_all_rotations_of_sequence([1, 2, 3, 4], -1))
    assert rotations == [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]


def test_sequencetools_yield_all_rotations_of_sequence_02():
    '''Yield all rotations of tuple.
    '''

    rotations = list(sequencetools.yield_all_rotations_of_sequence((1, 2, 3, 4), -1))
    assert rotations == [(1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, 3)]
