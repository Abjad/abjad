from abjad import *
from abjad.tools import seqtools


def test_seqtools_is_restricted_growth_function_01( ):

    assert seqtools.is_restricted_growth_function([1, 1, 1, 1])
    assert seqtools.is_restricted_growth_function([1, 1, 1, 2])
    assert seqtools.is_restricted_growth_function([1, 1, 2, 1])
    assert seqtools.is_restricted_growth_function([1, 1, 2, 2])
    assert seqtools.is_restricted_growth_function([1, 1, 2, 3])
    assert seqtools.is_restricted_growth_function([1, 2, 1, 1])
    assert seqtools.is_restricted_growth_function([1, 2, 1, 2])
    assert seqtools.is_restricted_growth_function([1, 2, 1, 3])
    assert seqtools.is_restricted_growth_function([1, 2, 2, 1])
    assert seqtools.is_restricted_growth_function([1, 2, 2, 2])
    assert seqtools.is_restricted_growth_function([1, 2, 2, 3])
    assert seqtools.is_restricted_growth_function([1, 2, 3, 1])
    assert seqtools.is_restricted_growth_function([1, 2, 3, 2])
    assert seqtools.is_restricted_growth_function([1, 2, 3, 3])
    assert seqtools.is_restricted_growth_function([1, 2, 3, 4])


def test_seqtools_is_restricted_growth_function_02( ):

    assert not seqtools.is_restricted_growth_function([1, 1, 1, 3])
    assert not seqtools.is_restricted_growth_function([1, 1, 3, 3])
    assert not seqtools.is_restricted_growth_function([1, 3, 1, 3])
    assert not seqtools.is_restricted_growth_function([3, 1, 1, 3])
