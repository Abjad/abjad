# -*- coding: utf-8 -*-
from abjad.tools import mathtools


def test_mathtools_Ratio___eq___01():

    ratio_1 = mathtools.Ratio((1, 2, 1))
    ratio_2 = mathtools.Ratio((1, 2, 1))
    ratio_3 = mathtools.Ratio((2, 3, 3))

    assert ratio_1 == ratio_1
    assert ratio_1 == ratio_2
    assert not ratio_1 == ratio_3
    assert ratio_2 == ratio_1
    assert ratio_2 == ratio_2
    assert not ratio_2 == ratio_3
    assert not ratio_3 == ratio_1
    assert not ratio_3 == ratio_2
    assert ratio_3 == ratio_3