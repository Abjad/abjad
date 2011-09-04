from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_yield_all_unordered_pairs_of_sequence_01():
    '''Handles input of length greater than 2.'''

    t = list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 2, 3, 4]))
    assert t == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


def test_sequencetools_yield_all_unordered_pairs_of_sequence_02():
    '''Handles input of length 2.'''

    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 2])) == [(1, 2)]


def test_sequencetools_yield_all_unordered_pairs_of_sequence_03():
    '''Handles input of length less than 2.'''

    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1])) == []
    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([])) == []


def test_sequencetools_yield_all_unordered_pairs_of_sequence_04():
    '''Handles set input. Note that we can't control
    the order in which the elements in set are iterated.
    So we must test result as an unordered set rather
    than an ordered list.'''

    t = set([1, 2, 3])
    result = list(sequencetools.yield_all_unordered_pairs_of_sequence(t) )
    assert set(result) == set([(1, 2), (1, 3), (2, 3)])


def test_sequencetools_yield_all_unordered_pairs_of_sequence_05():
    '''Handles duplicate input values.'''

    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 1])) == [(1, 1)]
    assert list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 1, 1])) == [(1, 1), (1, 1), (1, 1)]
