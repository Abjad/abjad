from abjad import *
from abjad.tools import seqtools


def test_seqtools_partition_sequence_once_by_counts_with_overhang_01():
    '''Partition sequence by positive counts.
    '''

    parts = seqtools.partition_sequence_once_by_counts_with_overhang(range(16), [4, 6])
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]


def test_seqtools_partition_sequence_once_by_counts_with_overhang_02():
    '''Partition sequence by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = seqtools.partition_sequence_once_by_counts_with_overhang(range(10), counts)
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5], [6, 7, 8, 9]]
