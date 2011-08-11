from abjad import *
from abjad.tools import seqtools


def test_seqtools_split_sequence_extended_to_weights_without_overhang_01( ):

    parts = seqtools.split_sequence_extended_to_weights_without_overhang([1, 2, 3, 4, 5], [7, 7, 7])

    assert parts == [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3]]
