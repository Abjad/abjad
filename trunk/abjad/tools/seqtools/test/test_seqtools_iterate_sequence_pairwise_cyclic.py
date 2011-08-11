from abjad import *
from abjad.tools import seqtools


def test_seqtools_iterate_sequence_pairwise_cyclic_01( ):
    '''Cyclic pairwise.'''

    t = range(6)
    pairs = seqtools.iterate_sequence_pairwise_cyclic(t)
    for x in range(100):
        assert pairs.next( )
