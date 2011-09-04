from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_remove_subsequence_of_weight_at_index_01():
    '''Remove weighted subrun from l at index i.'''

    t = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
    result = sequencetools.remove_subsequence_of_weight_at_index(t, 8, 0)

    assert result == [4, 5, 1, 2, 5, 5, 6]


def test_sequencetools_remove_subsequence_of_weight_at_index_02():
    '''Remove weighted subrun from l at index i.'''

    t = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
    result = sequencetools.remove_subsequence_of_weight_at_index(t, 13, 4)

    assert result == [1, 1, 2, 3, 5, 5, 6]
