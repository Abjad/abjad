from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_is_permutation_01():

    assert sequencetools.is_permutation([3, 0, 1, 2])
    assert sequencetools.is_permutation([2, 3, 0, 1])
    assert sequencetools.is_permutation([0, 1, 2, 3])


def test_sequencetools_is_permutation_02():

    assert not sequencetools.is_permutation([0, 0, 1, 2])
    assert not sequencetools.is_permutation('foo')
    assert not sequencetools.is_permutation(7)


def test_sequencetools_is_permutation_03():

    assert sequencetools.is_permutation([3, 0, 1, 2], length = 4)
    assert not sequencetools.is_permutation([3, 0, 1, 2], length = 3)
    assert not sequencetools.is_permutation([3, 0, 1, 2], length = 5)
