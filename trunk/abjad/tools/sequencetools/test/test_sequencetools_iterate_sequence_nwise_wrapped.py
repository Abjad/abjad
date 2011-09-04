from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_iterate_sequence_nwise_wrapped_01():

    t = list(sequencetools.iterate_sequence_nwise_wrapped(range(6), 3))
    assert t == [(0, 1, 2), (1, 2, 3), (2, 3, 4),
        (3, 4, 5), (4, 5, 0), (5, 0, 1)]
