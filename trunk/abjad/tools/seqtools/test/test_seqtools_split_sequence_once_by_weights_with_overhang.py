from abjad import *
from abjad.tools import seqtools


def test_seqtools_split_sequence_once_by_weights_with_overhang_01():

    sequence = (10, -10, 10, -10)
    pieces = seqtools.split_sequence_once_by_weights_with_overhang(sequence, [3, 15, 3])
    assert pieces == [(3,), (7, -8), (-2, 1), (9, -10)]


def test_seqtools_split_sequence_once_by_weights_with_overhang_02():
    '''Even split with overhang produces no terminal empty piece.
    '''

    sequence = (10, -10, 10, -10)
    pieces = seqtools.split_sequence_once_by_weights_with_overhang(sequence, [20])
    assert pieces == [(10, -10), (10, -10)]
