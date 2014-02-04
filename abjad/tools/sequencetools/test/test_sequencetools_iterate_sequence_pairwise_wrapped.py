# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_iterate_sequence_pairwise_wrapped_01():

    sequence = range(6)
    pairs = sequencetools.iterate_sequence_pairwise_wrapped(sequence)
    assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
