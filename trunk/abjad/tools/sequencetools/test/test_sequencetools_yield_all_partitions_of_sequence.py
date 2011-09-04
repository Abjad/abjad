from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_yield_all_partitions_of_sequence_01():

    assert list(sequencetools.yield_all_partitions_of_sequence([0, 1, 2])) == [
        [[0, 1, 2]],
        [[0, 1], [2]],
        [[0], [1, 2]],
        [[0], [1], [2]]
        ]


def test_sequencetools_yield_all_partitions_of_sequence_02():

    assert list(sequencetools.yield_all_partitions_of_sequence([0, 1, 2, 3])) == [
        [[0, 1, 2, 3]],
        [[0, 1, 2], [3]],
        [[0, 1], [2, 3]],
        [[0, 1], [2], [3]],
        [[0], [1, 2, 3]],
        [[0], [1, 2], [3]],
        [[0], [1], [2, 3]],
        [[0], [1], [2], [3]],
    ]
