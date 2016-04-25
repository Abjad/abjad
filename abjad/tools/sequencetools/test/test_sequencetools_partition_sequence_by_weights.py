# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_partition_sequence_by_weights_01():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [3, 9],
        cyclic=False,
        overhang=True,
        )
    assert groups == [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]


def test_sequencetools_partition_sequence_by_weights_02():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [3, 9],
        cyclic=False,
        overhang=False,
        )
    assert groups == [[3], [3, 3, 3]]


def test_sequencetools_partition_sequence_by_weights_03():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [12],
        cyclic=True,
        overhang=True,
        )
    assert groups == [[3, 3, 3, 3], [4, 4, 4], [4, 5]]


def test_sequencetools_partition_sequence_by_weights_04():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [12],
        cyclic=True,
        overhang=False,
        )
    assert groups == [[3, 3, 3, 3], [4, 4, 4]]


def test_sequencetools_partition_sequence_by_weights_05():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 4],
        cyclic=False,
        overhang=True,
        allow_part_weights=Less,
        )
    assert groups == [[3, 3, 3], [3], [4, 4, 4, 4, 5, 5]]


def test_sequencetools_partition_sequence_by_weights_06():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 4],
        cyclic=False,
        overhang=False,
        allow_part_weights=Less,
        )
    assert groups == [[3, 3, 3], [3]]


def test_sequencetools_partition_sequence_by_weights_07():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 5],
        cyclic=True,
        overhang=True,
        allow_part_weights=Less,
        )
    assert groups == [[3, 3, 3], [3], [4, 4], [4], [4, 5], [5]]


def test_sequencetools_partition_sequence_by_weights_08():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 5],
        cyclic=True,
        overhang=False,
        allow_part_weights=Less,
        )
    assert groups == [[3, 3, 3], [3], [4, 4], [4]]


def test_sequencetools_partition_sequence_by_weights_09():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 4],
        cyclic=False,
        overhang=True,
        allow_part_weights=More,
        )
    assert groups == [[3, 3, 3, 3], [4], [4, 4, 4, 5, 5]]


def test_sequencetools_partition_sequence_by_weights_10():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 4],
        cyclic=False,
        overhang=False,
        allow_part_weights=More,
        )
    assert groups == [[3, 3, 3, 3], [4]]


def test_sequencetools_partition_sequence_by_weights_11():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 4],
        cyclic=True,
        overhang=True,
        allow_part_weights=More,
        )
    assert groups == [[3, 3, 3, 3], [4], [4, 4, 4], [5], [5]]


def test_sequencetools_partition_sequence_by_weights_12():

    sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    groups = sequencetools.partition_sequence_by_weights(
        sequence,
        [10, 4],
        cyclic=True,
        overhang=False,
        allow_part_weights=More,
        )
    assert groups == [[3, 3, 3, 3], [4], [4, 4, 4], [5]]
