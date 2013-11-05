# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_partition_sequence_by_counts_01():
    r'''Partition sequence by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(range(16), [4, 6], cyclic=True, overhang=True)
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13], [14, 15]]


def test_sequencetools_partition_sequence_by_counts_02():
    r'''Partition sequence by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(range(10), counts, cyclic=True, overhang=True)
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5], [], [6, 7], [], [], [8, 9]]



def test_sequencetools_partition_sequence_by_counts_03():
    r'''Partition sequence by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(range(16), [4, 6], cyclic=True, overhang=False)
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13]]


def test_sequencetools_partition_sequence_by_counts_04():
    r'''Partition sequence by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(range(10), counts, cyclic=True, overhang=False)
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5], [], [6, 7], [], []]



def test_sequencetools_partition_sequence_by_counts_05():
    r'''Partition sequence by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(range(16), [4, 6], cyclic=False, overhang=True)
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]


def test_sequencetools_partition_sequence_by_counts_06():
    r'''Partition sequence by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(range(10), counts, cyclic=False, overhang=True)
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5], [6, 7, 8, 9]]


def test_sequencetools_partition_sequence_by_counts_07():
    r'''Partition list by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(range(16), [4, 6], cyclic=False, overhang=False)
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9]]


def test_sequencetools_partition_sequence_by_counts_08():
    r'''Partition list by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(range(10), counts, cyclic=False, overhang=False)
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5]]


def test_sequencetools_partition_sequence_by_counts_09():
    r'''Partition Abjad container.
    '''

    container = Container("c'8 d'8 e'8 f'8 g'8 a'8")
    parts = sequencetools.partition_sequence_by_counts(container, [1, 2], cyclic=False, overhang=False)

    "[{c'8}, {d'8, e'8}]"

    assert len(parts) == 2
    assert format(parts[0]) == format(Container("c'8"))
    assert parts[0][0] is not container[0]
    assert format(parts[1]) == format(Container("d'8 e'8"))
    assert parts[1][0] is not container[1]
    assert parts[1][1] is not container[2]


def test_sequencetools_partition_sequence_by_counts_10():
    r'''Partition list of arbitrary objects instead of just integers.
    '''

    parts = sequencetools.partition_sequence_by_counts('this is text', [1, 3], cyclic=True, overhang=True)
    assert parts == ['t', 'his', ' ', 'is ', 't', 'ext']
