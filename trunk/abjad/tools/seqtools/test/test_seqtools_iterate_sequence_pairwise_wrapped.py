from abjad import *
from abjad.tools import seqtools


def test_seqtools_iterate_sequence_pairwise_wrapped_01( ):
    '''Wrapped pairwise.
    '''

    t = range(6)
    pairs = seqtools.iterate_sequence_pairwise_wrapped(t)
    assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
