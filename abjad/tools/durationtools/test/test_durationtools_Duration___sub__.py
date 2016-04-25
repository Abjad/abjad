# -*- coding: utf-8 -*-
from abjad import *


def test_durationtools_Duration___sub___01():
    r'''Subtracting nonreduced fraction from duration
    returns nonreduced fraction.
    '''

    result = Duration(1, 2) - mathtools.NonreducedFraction(2, 8)
    assert isinstance(result, mathtools.NonreducedFraction)
    assert result.pair == (2, 8)


def test_durationtools_Duration___sub___02():
    r'''Subtracting duration from nonreduced fraction
    returns nonreduced fraction.
    '''

    result = mathtools.NonreducedFraction(4, 8) - Duration(1, 4)
    assert isinstance(result, mathtools.NonreducedFraction)
    assert result.pair == (2, 8)
