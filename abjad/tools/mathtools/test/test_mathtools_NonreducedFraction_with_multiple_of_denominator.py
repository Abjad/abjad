# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_NonreducedFraction_with_multiple_of_denominator_01():

    duration = Duration(1, 2)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(2) == mathtools.NonreducedFraction(1, 2)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(4) == mathtools.NonreducedFraction(2, 4)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(8) == mathtools.NonreducedFraction(4, 8)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(16) == mathtools.NonreducedFraction(8, 16)


def test_mathtools_NonreducedFraction_with_multiple_of_denominator_02():

    duration = Duration(1, 2)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(3) == mathtools.NonreducedFraction(3, 6)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(6) == mathtools.NonreducedFraction(3, 6)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(12) == mathtools.NonreducedFraction(6, 12)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(24) == mathtools.NonreducedFraction(12, 24)


def test_mathtools_NonreducedFraction_with_multiple_of_denominator_03():

    duration = Duration(1, 2)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(5) == mathtools.NonreducedFraction(5, 10)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(10) == mathtools.NonreducedFraction(5, 10)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(20) == mathtools.NonreducedFraction(10, 20)
    assert mathtools.NonreducedFraction(duration).with_multiple_of_denominator(40) == mathtools.NonreducedFraction(20, 40)
