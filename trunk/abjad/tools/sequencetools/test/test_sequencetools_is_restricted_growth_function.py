from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_is_restricted_growth_function_01():

    assert sequencetools.is_restricted_growth_function([1, 1, 1, 1])
    assert sequencetools.is_restricted_growth_function([1, 1, 1, 2])
    assert sequencetools.is_restricted_growth_function([1, 1, 2, 1])
    assert sequencetools.is_restricted_growth_function([1, 1, 2, 2])
    assert sequencetools.is_restricted_growth_function([1, 1, 2, 3])
    assert sequencetools.is_restricted_growth_function([1, 2, 1, 1])
    assert sequencetools.is_restricted_growth_function([1, 2, 1, 2])
    assert sequencetools.is_restricted_growth_function([1, 2, 1, 3])
    assert sequencetools.is_restricted_growth_function([1, 2, 2, 1])
    assert sequencetools.is_restricted_growth_function([1, 2, 2, 2])
    assert sequencetools.is_restricted_growth_function([1, 2, 2, 3])
    assert sequencetools.is_restricted_growth_function([1, 2, 3, 1])
    assert sequencetools.is_restricted_growth_function([1, 2, 3, 2])
    assert sequencetools.is_restricted_growth_function([1, 2, 3, 3])
    assert sequencetools.is_restricted_growth_function([1, 2, 3, 4])


def test_sequencetools_is_restricted_growth_function_02():

    assert not sequencetools.is_restricted_growth_function([1, 1, 1, 3])
    assert not sequencetools.is_restricted_growth_function([1, 1, 3, 3])
    assert not sequencetools.is_restricted_growth_function([1, 3, 1, 3])
    assert not sequencetools.is_restricted_growth_function([3, 1, 1, 3])
