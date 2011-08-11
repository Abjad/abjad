from abjad import *
from abjad.tools import seqtools


def test_seqtools_yield_all_partitions_of_sequence_01( ):

    assert list(seqtools.yield_all_partitions_of_sequence([0, 1, 2])) == [
        [[0, 1, 2]],
        [[0, 1], [2]],
        [[0], [1, 2]],
        [[0], [1], [2]]
        ]


def test_seqtools_yield_all_partitions_of_sequence_02( ):

    assert list(seqtools.yield_all_partitions_of_sequence([0, 1, 2, 3])) == [
        [[0, 1, 2, 3]],
        [[0, 1, 2], [3]],
        [[0, 1], [2, 3]],
        [[0, 1], [2], [3]],
        [[0], [1, 2, 3]],
        [[0], [1, 2], [3]],
        [[0], [1], [2, 3]],
        [[0], [1], [2], [3]],
    ]
