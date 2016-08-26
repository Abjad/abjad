# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_partition_sequence_by_weights_01():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [3, 9],
        cyclic=False,
        overhang=True,
        )
    assert parts == [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [3, 9],
        cyclic=False,
        overhang=True,
        )
    assert parts == [[-3], [-3, -3, -3], [-4, -4, -4, -4, -5, -5]]


def test_sequencetools_partition_sequence_by_weights_02():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [3, 9],
        cyclic=False,
        overhang=False,
        )
    assert parts == [[3], [3, 3, 3]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [3, 9],
        cyclic=False,
        overhang=False,
        )
    assert parts == [[-3], [-3, -3, -3]]


def test_sequencetools_partition_sequence_by_weights_03():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [12],
        cyclic=True,
        overhang=True,
        )
    assert parts == [[3, 3, 3, 3], [4, 4, 4], [4, 5]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [12],
        cyclic=True,
        overhang=True,
        )
    assert parts == [[-3, -3, -3, -3], [-4, -4, -4], [-4, -5]]


def test_sequencetools_partition_sequence_by_weights_04():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [12],
        cyclic=True,
        overhang=False,
        )
    assert parts == [[3, 3, 3, 3], [4, 4, 4]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [12],
        cyclic=True,
        overhang=False,
        )
    assert parts == [[-3, -3, -3, -3], [-4, -4, -4]]


def test_sequencetools_partition_sequence_by_weights_05():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=False,
        overhang=True,
        allow_part_weights=Less,
        )
    assert parts == [[3, 3, 3], [3], [4, 4, 4, 4, 5, 5]]


def test_sequencetools_partition_sequence_by_weights_06():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=False,
        overhang=False,
        allow_part_weights=Less,
        )
    assert parts == [[3, 3, 3], [3]]


def test_sequencetools_partition_sequence_by_weights_07():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 5],
        cyclic=True,
        overhang=True,
        allow_part_weights=Less,
        )
    assert parts == [[3, 3, 3], [3], [4, 4], [4], [4, 5], [5]]


def test_sequencetools_partition_sequence_by_weights_08():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 5],
        cyclic=True,
        overhang=False,
        allow_part_weights=Less,
        )
    assert parts == [[3, 3, 3], [3], [4, 4], [4]]


def test_sequencetools_partition_sequence_by_weights_09():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=False,
        overhang=True,
        allow_part_weights=More,
        )
    assert parts == [[3, 3, 3, 3], [4], [4, 4, 4, 5, 5]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=False,
        overhang=True,
        allow_part_weights=More,
        )
    assert parts == [[-3, -3, -3, -3], [-4], [-4, -4, -4, -5, -5]]


def test_sequencetools_partition_sequence_by_weights_10():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=False,
        overhang=False,
        allow_part_weights=More,
        )
    assert parts == [[3, 3, 3, 3], [4]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=False,
        overhang=False,
        allow_part_weights=More,
        )
    assert parts == [[-3, -3, -3, -3], [-4]]


def test_sequencetools_partition_sequence_by_weights_11():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=True,
        overhang=True,
        allow_part_weights=More,
        )
    assert parts == [[3, 3, 3, 3], [4], [4, 4, 4], [5], [5]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=True,
        overhang=True,
        allow_part_weights=More,
        )
    assert parts == [[-3, -3, -3, -3], [-4], [-4, -4, -4], [-5], [-5]]


def test_sequencetools_partition_sequence_by_weights_12():

    list_ = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=True,
        overhang=False,
        allow_part_weights=More,
        )
    assert parts == [[3, 3, 3, 3], [4], [4, 4, 4], [5]]

    list_ = [-1 * _ for _ in list_]
    parts = sequencetools.partition_sequence_by_weights(
        list_,
        [10, 4],
        cyclic=True,
        overhang=False,
        allow_part_weights=More,
        )
    assert parts == [[-3, -3, -3, -3], [-4], [-4, -4, -4], [-5]]