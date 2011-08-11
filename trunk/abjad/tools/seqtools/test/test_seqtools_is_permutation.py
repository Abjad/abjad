from abjad import *
from abjad.tools import seqtools


def test_seqtools_is_permutation_01( ):

    assert seqtools.is_permutation([3, 0, 1, 2])
    assert seqtools.is_permutation([2, 3, 0, 1])
    assert seqtools.is_permutation([0, 1, 2, 3])


def test_seqtools_is_permutation_02( ):

    assert not seqtools.is_permutation([0, 0, 1, 2])
    assert not seqtools.is_permutation('foo')
    assert not seqtools.is_permutation(7)


def test_seqtools_is_permutation_03( ):

    assert seqtools.is_permutation([3, 0, 1, 2], length = 4)
    assert not seqtools.is_permutation([3, 0, 1, 2], length = 3)
    assert not seqtools.is_permutation([3, 0, 1, 2], length = 5)
