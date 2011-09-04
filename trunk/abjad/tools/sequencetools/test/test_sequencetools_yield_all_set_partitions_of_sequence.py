from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_yield_all_set_partitions_of_sequence_01():

    l = [1, 2, 3, 4]
    set_partitions = sequencetools.yield_all_set_partitions_of_sequence(l)

    assert set_partitions.next() == [[1, 2, 3, 4]]
    assert set_partitions.next() == [[1, 2, 3], [4]]
    assert set_partitions.next() == [[1, 2, 4], [3]]
    assert set_partitions.next() == [[1, 2], [3, 4]]
    assert set_partitions.next() == [[1, 2], [3], [4]]
    assert set_partitions.next() == [[1, 3, 4], [2]]
    assert set_partitions.next() == [[1, 3], [2, 4]]
    assert set_partitions.next() == [[1, 3], [2], [4]]
    assert set_partitions.next() == [[1, 4], [2, 3]]
    assert set_partitions.next() == [[1], [2, 3, 4]]
    assert set_partitions.next() == [[1], [2, 3], [4]]
    assert set_partitions.next() == [[1, 4], [2], [3]]
    assert set_partitions.next() == [[1], [2, 4], [3]]
    assert set_partitions.next() == [[1], [2], [3, 4]]
    assert set_partitions.next() == [[1], [2], [3], [4]]
