from abjad import *
from abjad.tools import seqtools


def test_seqtools_all_are_nonnegative_integers_01( ):

    assert seqtools.all_are_nonnegative_integers([0, 1, 2, 3, 99])


def test_seqtools_all_are_nonnegative_integers_02( ):

    assert not seqtools.all_are_nonnegative_integers([-1, 2, 3, 99])
    assert not seqtools.all_are_nonnegative_integers(7)
    assert not seqtools.all_are_nonnegative_integers('foo')
