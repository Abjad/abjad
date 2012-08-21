from abjad import *


def test_sequencetools_partition_sequence_by_weights_at_most_01():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights_at_most(
        sequence, [10, 4], cyclic=False, overhang=True)
    assert groups == [[3, 3, 3], [3], [4, 4, 4, 4, 5, 5]]


def test_sequencetools_partition_sequence_by_weights_at_most_02():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights_at_most(
        sequence, [10, 4], cyclic=False, overhang=False)
    assert groups == [[3, 3, 3], [3]] 


def test_sequencetools_partition_sequence_by_weights_at_most_03():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights_at_most(
        sequence, [10, 5], cyclic=True, overhang=True)
    assert groups == [[3, 3, 3], [3], [4, 4], [4], [4, 5], [5]]


def test_sequencetools_partition_sequence_by_weights_at_most_04():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5] 
    groups = sequencetools.partition_sequence_by_weights_at_most(
        sequence, [10, 5], cyclic=True, overhang=False)
    assert groups == [[3, 3, 3], [3], [4, 4], [4]] 
