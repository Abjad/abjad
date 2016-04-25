# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_all_are_positive_integers_01():

    assert mathtools.all_are_positive_integers([1, 2, 3, 99])


def test_mathtools_all_are_positive_integers_02():

    assert not mathtools.all_are_positive_integers([0, 2, 3, 99])
    assert not mathtools.all_are_positive_integers([-1, 2, 3, 99])
    assert not mathtools.all_are_positive_integers(7)
    assert not mathtools.all_are_positive_integers('foo')
