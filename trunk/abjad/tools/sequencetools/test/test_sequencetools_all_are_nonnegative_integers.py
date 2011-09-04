from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_nonnegative_integers_01():

    assert sequencetools.all_are_nonnegative_integers([0, 1, 2, 3, 99])


def test_sequencetools_all_are_nonnegative_integers_02():

    assert not sequencetools.all_are_nonnegative_integers([-1, 2, 3, 99])
    assert not sequencetools.all_are_nonnegative_integers(7)
    assert not sequencetools.all_are_nonnegative_integers('foo')
