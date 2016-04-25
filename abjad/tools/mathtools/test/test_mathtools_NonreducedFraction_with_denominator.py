# -*- coding: utf-8 -*-
from abjad import *


def test_mathtools_NonreducedFraction_with_denominator_01():
    assert mathtools.NonreducedFraction((0, 6)).with_denominator(12) == mathtools.NonreducedFraction(0, 12)
    assert mathtools.NonreducedFraction((1, 6)).with_denominator(12) == mathtools.NonreducedFraction(2, 12)
    assert mathtools.NonreducedFraction((2, 6)).with_denominator(12) == mathtools.NonreducedFraction(4, 12)
    assert mathtools.NonreducedFraction((3, 6)).with_denominator(12) == mathtools.NonreducedFraction(6, 12)
    assert mathtools.NonreducedFraction((4, 6)).with_denominator(12) == mathtools.NonreducedFraction(8, 12)
    assert mathtools.NonreducedFraction((5, 6)).with_denominator(12) == mathtools.NonreducedFraction(10, 12)
    assert mathtools.NonreducedFraction((6, 6)).with_denominator(12) == mathtools.NonreducedFraction(12, 12)
    assert mathtools.NonreducedFraction((7, 6)).with_denominator(12) == mathtools.NonreducedFraction(14, 12)
    assert mathtools.NonreducedFraction((8, 6)).with_denominator(12) == mathtools.NonreducedFraction(16, 12)
    assert mathtools.NonreducedFraction((9, 6)).with_denominator(12) == mathtools.NonreducedFraction(18, 12)
    assert mathtools.NonreducedFraction((10, 6)).with_denominator(12) == mathtools.NonreducedFraction(20, 12)
    assert mathtools.NonreducedFraction((11, 6)).with_denominator(12) == mathtools.NonreducedFraction(22, 12)


def test_mathtools_NonreducedFraction_with_denominator_02():
    assert mathtools.NonreducedFraction((0, 12)).with_denominator(6) == mathtools.NonreducedFraction(0, 6)
    assert mathtools.NonreducedFraction((1, 12)).with_denominator(6) == mathtools.NonreducedFraction(1, 12)
    assert mathtools.NonreducedFraction((2, 12)).with_denominator(6) == mathtools.NonreducedFraction(1, 6)
    assert mathtools.NonreducedFraction((3, 12)).with_denominator(6) == mathtools.NonreducedFraction(3, 12)
    assert mathtools.NonreducedFraction((4, 12)).with_denominator(6) == mathtools.NonreducedFraction(2, 6)
    assert mathtools.NonreducedFraction((5, 12)).with_denominator(6) == mathtools.NonreducedFraction(5, 12)
    assert mathtools.NonreducedFraction((6, 12)).with_denominator(6) == mathtools.NonreducedFraction(3, 6)
    assert mathtools.NonreducedFraction((7, 12)).with_denominator(6) == mathtools.NonreducedFraction(7, 12)
    assert mathtools.NonreducedFraction((8, 12)).with_denominator(6) == mathtools.NonreducedFraction(4, 6)
    assert mathtools.NonreducedFraction((9, 12)).with_denominator(6) == mathtools.NonreducedFraction(9, 12)
    assert mathtools.NonreducedFraction((10, 12)).with_denominator(6) == mathtools.NonreducedFraction(5, 6)
    assert mathtools.NonreducedFraction((11, 12)).with_denominator(6) == mathtools.NonreducedFraction(11, 12)


def test_mathtools_NonreducedFraction_with_denominator_03():
    assert mathtools.NonreducedFraction((0, 12)).with_denominator(8) == mathtools.NonreducedFraction(0, 8)
    assert mathtools.NonreducedFraction((1, 12)).with_denominator(8) == mathtools.NonreducedFraction(1, 12)
    assert mathtools.NonreducedFraction((2, 12)).with_denominator(8) == mathtools.NonreducedFraction(2, 12)
    assert mathtools.NonreducedFraction((3, 12)).with_denominator(8) == mathtools.NonreducedFraction(2, 8)
    assert mathtools.NonreducedFraction((4, 12)).with_denominator(8) == mathtools.NonreducedFraction(4, 12)
    assert mathtools.NonreducedFraction((5, 12)).with_denominator(8) == mathtools.NonreducedFraction(5, 12)
    assert mathtools.NonreducedFraction((6, 12)).with_denominator(8) == mathtools.NonreducedFraction(4, 8)
    assert mathtools.NonreducedFraction((7, 12)).with_denominator(8) == mathtools.NonreducedFraction(7, 12)
    assert mathtools.NonreducedFraction((8, 12)).with_denominator(8) == mathtools.NonreducedFraction(8, 12)
    assert mathtools.NonreducedFraction((9, 12)).with_denominator(8) == mathtools.NonreducedFraction(6, 8)
    assert mathtools.NonreducedFraction((10, 12)).with_denominator(8) == mathtools.NonreducedFraction(10, 12)
    assert mathtools.NonreducedFraction((11, 12)).with_denominator(8) == mathtools.NonreducedFraction(11, 12)
