from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_all_are_positive_integers_01():

    assert sequencetools.all_are_positive_integers([1, 2, 3, 99])


def test_sequencetools_all_are_positive_integers_02():

    assert not sequencetools.all_are_positive_integers([0, 2, 3, 99])
    assert not sequencetools.all_are_positive_integers([-1, 2, 3, 99])
    assert not sequencetools.all_are_positive_integers(7)
    assert not sequencetools.all_are_positive_integers('foo')
