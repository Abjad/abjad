from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_yield_all_subsequences_of_sequence_01():

    l = range(10)
    sublists = list(sequencetools.yield_all_subsequences_of_sequence(l, 4, 5))

    assert len(sublists) == 13
    assert sublists[0] == [0, 1, 2, 3]
    assert sublists[1] == [0, 1, 2, 3, 4]
    assert sublists[2] == [1, 2, 3, 4]
    assert sublists[3] == [1, 2, 3, 4, 5]
    assert sublists[4] == [2, 3, 4, 5]
    assert sublists[5] == [2, 3, 4, 5, 6]
    assert sublists[6] == [3, 4, 5, 6]
    assert sublists[7] == [3, 4, 5, 6, 7]
    assert sublists[8] == [4, 5, 6, 7]
    assert sublists[9] == [4, 5, 6, 7, 8]
    assert sublists[10] == [5, 6, 7, 8]
    assert sublists[11] == [5, 6, 7, 8, 9]
    assert sublists[12] == [6, 7, 8, 9]


def test_sequencetools_yield_all_subsequences_of_sequence_02():

    assert list(sequencetools.yield_all_subsequences_of_sequence([0, 1, 2])) == [
        [], [0], [0, 1], [0, 1, 2], [1], [1, 2], [2]]
