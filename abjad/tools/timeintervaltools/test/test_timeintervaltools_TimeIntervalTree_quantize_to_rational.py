# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *
import pytest


def test_timeintervaltools_TimeIntervalTree_quantize_to_rational_01():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = tree.quantize_to_rational(1)
    assert result == \
    TimeIntervalTree([
        TimeInterval(Fraction(0, 1), Fraction(1, 1), {}),
        TimeInterval(Fraction(0, 1), Fraction(2, 1), {})
    ])


def test_timeintervaltools_TimeIntervalTree_quantize_to_rational_02():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = tree.quantize_to_rational(Fraction(1, 4))
    assert result == \
    TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(1, 1), {}),
        TimeInterval(Fraction(1, 4), Fraction(7, 4), {})
    ])


def test_timeintervaltools_TimeIntervalTree_quantize_to_rational_03():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = tree.quantize_to_rational(Fraction(2, 5))
    assert result == \
    TimeIntervalTree([
        TimeInterval(Fraction(2, 5), Fraction(4, 5), {}),
        TimeInterval(Fraction(2, 5), Fraction(8, 5), {})
    ])


def test_timeintervaltools_TimeIntervalTree_quantize_to_rational_04():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    pytest.raises(AssertionError, "result = tree.quantize_to_rational(0)")


def test_timeintervaltools_TimeIntervalTree_quantize_to_rational_05():
    tree = TimeIntervalTree([])
    result = tree.quantize_to_rational(1)
    assert result == tree
    
