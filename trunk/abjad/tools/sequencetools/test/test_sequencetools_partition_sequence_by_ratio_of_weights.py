from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_partition_sequence_by_ratio_of_weights_01():
    '''Common cases.'''

    l = [1] * 10

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [1, 1, 1])
    assert result == [[1, 1, 1], [1, 1, 1, 1], [1, 1, 1]]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [1, 1, 1, 1])
    assert result == [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1]]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [2, 2, 3])
    assert result == [[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [3, 2, 2])
    assert result == [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1]]


def test_sequencetools_partition_sequence_by_ratio_of_weights_02():
    '''Unusual cases.'''

    l = [5, 5]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [1, 1, 1])
    assert result == [[5], [5], []]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [1, 1, 1, 1])
    assert result == [[5], [], [5], []]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [2, 2, 3])
    assert result == [[5], [5], []]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [3, 2, 2])
    assert result == [[5], [5], []]


def test_sequencetools_partition_sequence_by_ratio_of_weights_03():
    '''More unusual cases.'''

    l = [7, 3]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [1, 1, 1])
    assert result == [[7], [], [3]]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [1, 1, 1, 1])
    assert result == [[7], [], [3], []]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [2, 2, 3])
    assert result == [[7], [], [3]]

    result = sequencetools.partition_sequence_by_ratio_of_weights(l, [3, 2, 2])
    assert result == [[7], [], [3]]
