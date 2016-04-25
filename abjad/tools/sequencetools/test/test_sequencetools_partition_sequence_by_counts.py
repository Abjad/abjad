# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_sequencetools_partition_sequence_by_counts_01():
    r'''Partitions sequence by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(
        list(range(16)),
        [4, 6],
        cyclic=True,
        overhang=True,
        )
    assert parts == [
        [0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13], [14, 15]]


def test_sequencetools_partition_sequence_by_counts_02():
    r'''Partitions sequence by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(
        list(range(10)),
        counts,
        cyclic=True,
        overhang=True,
        )
    assert parts == [
        [], [0, 1], [], [], [2, 3, 4, 5], [], [6, 7], [], [], [8, 9]]


def test_sequencetools_partition_sequence_by_counts_03():
    r'''Partitions sequence by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(
        list(range(16)),
        [4, 6],
        cyclic=True,
        overhang=False,
        )
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13]]


def test_sequencetools_partition_sequence_by_counts_04():
    r'''Partitions sequence by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(
        list(range(10)),
        counts,
        cyclic=True,
        overhang=False,
        )
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5], [], [6, 7], [], []]


def test_sequencetools_partition_sequence_by_counts_05():
    r'''Partitions sequence by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(
        list(range(16)),
        [4, 6],
        cyclic=False,
        overhang=True,
        )
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]


def test_sequencetools_partition_sequence_by_counts_06():
    r'''Partitions sequence by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(
        list(range(10)),
        counts,
        cyclic=False,
        overhang=True,
        )
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5], [6, 7, 8, 9]]


def test_sequencetools_partition_sequence_by_counts_07():
    r'''Partitions list by positive counts.
    '''

    parts = sequencetools.partition_sequence_by_counts(
        list(range(16)),
        [4, 6],
        cyclic=False,
        overhang=False,
        )
    assert parts == [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9]]


def test_sequencetools_partition_sequence_by_counts_08():
    r'''Partitions list by nonnegative counts.
    '''

    counts = (0, 2, 0, 0, 4)
    parts = sequencetools.partition_sequence_by_counts(
        list(range(10)),
        counts,
        cyclic=False,
        overhang=False,
        )
    assert parts == [[], [0, 1], [], [], [2, 3, 4, 5]]


def test_sequencetools_partition_sequence_by_counts_09():
    r'''Partitions string.
    '''

    parts = sequencetools.partition_sequence_by_counts(
        'this is text',
        [1, 3],
        cyclic=True,
        overhang=True,
        )
    assert parts == ['t', 'his', ' ', 'is ', 't', 'ext']


def test_sequencetools_partition_sequence_by_counts_10():
    r'''Raises exception when sequence does not partition exactly.
    '''

    string = 'sequencetools.partition_sequence_by_counts(list(range(10)), [3], cyclic=True, overhang=Exact)'
    assert pytest.raises(Exception, string)
