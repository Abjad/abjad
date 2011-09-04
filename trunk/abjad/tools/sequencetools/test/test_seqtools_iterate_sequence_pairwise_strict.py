from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_iterate_sequence_pairwise_strict_01():
    '''Pairwise list of numbers.'''
    t = range(6)
    pairs = sequencetools.iterate_sequence_pairwise_strict(t)
    assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]


def test_sequencetools_iterate_sequence_pairwise_strict_02():
    '''Pairwise list of notes.'''
    t = [Note(x, (1, 4)) for x in range(6)]
    pairs = sequencetools.iterate_sequence_pairwise_strict(t)
    for i, pair in enumerate(pairs):
        assert (pair[0], pair[1]) == (t[i], t[i + 1])


#def test_sequencetools_iterate_sequence_pairwise_strict_03():
#   '''Counted pairwise.'''
#   t = range(6)
#   pairs = sequencetools.iterate_sequence_pairwise_strict(t, 10)
#   assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
#      (5, 0), (0, 1), (1, 2), (2, 3), (3, 4)]


def test_sequencetools_iterate_sequence_pairwise_strict_04():
    '''Works on generators.'''
    t = xrange(6)
    pairs = sequencetools.iterate_sequence_pairwise_strict(t)
    pairs = list(pairs)
    assert pairs[0] == (0, 1)
    assert pairs[1] == (1, 2)
    assert pairs[2] == (2, 3)
    assert pairs[3] == (3, 4)
    assert pairs[4] == (4, 5)
