from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_partition_sequence_once_by_counts_without_overhang_01():
    '''Partition list by positive counts.
    '''

    parts = sequencetools.partition_sequence_once_by_counts_without_overhang(range(16), [4, 6])
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9]]


def test_sequencetools_partition_sequence_once_by_counts_without_overhang_02():
    '''Partition list by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_once_by_counts_without_overhang(range(10), counts)
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5]]


def test_sequencetools_partition_sequence_once_by_counts_without_overhang_03():
    '''Partition Abjad container.
    '''

    container = Container("c'8 d'8 e'8 f'8 g'8 a'8")
    parts = sequencetools.partition_sequence_once_by_counts_without_overhang(container, [1, 2])

    "[{c'8}, {d'8, e'8}]"

    assert len(parts) == 2
    assert parts[0].format == Container("c'8").format
    assert parts[0][0] is not container[0]
    assert parts[1].format == Container("d'8 e'8").format
    assert parts[1][0] is not container[1]
    assert parts[1][1] is not container[2]
