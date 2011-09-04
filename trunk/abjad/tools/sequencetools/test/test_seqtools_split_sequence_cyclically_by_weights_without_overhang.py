from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_split_sequence_cyclically_by_weights_without_overhang_01():

    sequence = (10, -10, 10, -10)
    pieces = sequencetools.split_sequence_cyclically_by_weights_without_overhang(sequence, [3, 15, 3])
    assert pieces == [(3,), (7, -8), (-2, 1), (3,), (6, -9)]
