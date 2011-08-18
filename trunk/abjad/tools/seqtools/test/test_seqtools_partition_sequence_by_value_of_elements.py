from abjad import *
from abjad.tools import seqtools


def test_seqtools_partition_sequence_by_value_of_elements_01():

    l = [ ]

    t = list(seqtools.partition_sequence_by_value_of_elements(l))
    assert t == [ ]


def test_seqtools_partition_sequence_by_value_of_elements_02():

    l = [1, 1, 1, 'a', 'a']

    t = list(seqtools.partition_sequence_by_value_of_elements(l))
    assert t == [(1, 1, 1), ('a', 'a')]


def test_seqtools_partition_sequence_by_value_of_elements_03():

    l = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]

    t = list(seqtools.partition_sequence_by_value_of_elements(l))
    assert t == [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)]
