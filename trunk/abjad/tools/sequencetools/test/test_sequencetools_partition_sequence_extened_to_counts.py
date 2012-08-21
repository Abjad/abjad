from abjad import *


def test_sequencetools_partition_sequence_extened_to_counts_01():

    parts = sequencetools.partition_sequence_extended_to_counts([1, 2, 3, 4], [6, 6, 6], overhang=True)

    assert parts == [[1, 2, 3, 4, 1, 2], [3, 4, 1, 2, 3, 4], [1, 2, 3, 4, 1, 2], [3, 4]]


def test_sequencetools_partition_sequence_extened_to_counts_02():

    parts = sequencetools.partition_sequence_extended_to_counts([1, 2, 3, 4], [6, 6, 6], overhang=False)

    assert parts == [[1, 2, 3, 4, 1, 2], [3, 4, 1, 2, 3, 4], [1, 2, 3, 4, 1, 2]]
