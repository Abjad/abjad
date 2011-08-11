from abjad import *
from abjad.tools import seqtools


def test_seqtools_yield_all_k_ary_sequences_of_length_01( ):

    generator = seqtools.yield_all_k_ary_sequences_of_length(2, 3)

    assert generator.next( ) == (0, 0, 0)
    assert generator.next( ) == (0, 0, 1)
    assert generator.next( ) == (0, 1, 0)
    assert generator.next( ) == (0, 1, 1)
    assert generator.next( ) == (1, 0, 0)
    assert generator.next( ) == (1, 0, 1)
    assert generator.next( ) == (1, 1, 0)
    assert generator.next( ) == (1, 1, 1)
