# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_split_sequence_01():

    sequence = (10, -10, 10, -10)
    shards = sequencetools.split_sequence(
        sequence,
        [3, 15, 3],
        cyclic=True, 
        overhang=True,
        )

    assert shards == ((3,), (7, -8), (-2, 1), (3,), (6, -9), (-1,))


def test_sequencetools_split_sequence_02():
    r'''Even split with overhang produces no terminal empty shard.
    '''

    sequence = (10, -10, 10, -10)
    shards = sequencetools.split_sequence(
        sequence,
        [20],
        cyclic=True, 
        overhang=True,
        )

    assert shards == ((10, -10), (10, -10))


def test_sequencetools_split_sequence_03():

    sequence = (10, -10, 10, -10)
    shards = sequencetools.split_sequence(
        sequence,
        [3, 15, 3],
        cyclic=True, 
        overhang=False,
        )

    assert shards == ((3,), (7, -8), (-2, 1), (3,), (6, -9))


def test_sequencetools_split_sequence_04():

    sequence = (10, -10, 10, -10)
    shards = sequencetools.split_sequence(
        sequence,
        [3, 15, 3],
        cyclic=False, 
        overhang=True,
        )

    assert shards == ((3,), (7, -8), (-2, 1), (9, -10))


def test_sequencetools_split_sequence_05():
    r'''Even split with overhang produces no terminal empty shard.
    '''

    sequence = (10, -10, 10, -10)
    shards = sequencetools.split_sequence(
        sequence,
        [20],
        cyclic=False, 
        overhang=True,
        )

    assert shards == ((10, -10), (10, -10))


def test_sequencetools_split_sequence_06():

    sequence = (10, -10, 10, -10)
    shards = sequencetools.split_sequence(
        sequence,
        [3, 15, 3],
        cyclic=False, 
        overhang=False,
        )

    assert shards == ((3, ), (7, -8), (-2, 1))
