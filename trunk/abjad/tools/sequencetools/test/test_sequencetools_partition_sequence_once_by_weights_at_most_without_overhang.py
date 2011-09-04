from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_partition_sequence_once_by_weights_at_most_without_overhang_01():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_once_by_weights_at_most_without_overhang(
        sequence, [10, 4])
    assert groups == [[3, 3, 3], [3]]
