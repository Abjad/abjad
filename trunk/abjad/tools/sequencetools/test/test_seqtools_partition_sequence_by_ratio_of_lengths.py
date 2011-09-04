from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_partition_sequence_by_ratio_of_lengths_01():

    parts = sequencetools.partition_sequence_by_ratio_of_lengths(range(10), [1, 1, 2])
    assert parts == [[0, 1, 2], [3, 4], [5, 6, 7, 8, 9]]
