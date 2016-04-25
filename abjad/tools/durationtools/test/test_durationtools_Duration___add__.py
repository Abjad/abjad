# -*- coding: utf-8 -*-
from abjad import *


def test_durationtools_Duration___add___01():
    r'''Adding two durations returns a third duration.
    '''

    duration = Duration(1, 2) + Duration(1, 3)
    assert isinstance(duration, Duration)


def test_durationtools_Duration___add___02():
    r'''Adding a duration and nonreduced fraction
    returns a nonreduced fraction.
    '''

    result = Duration(1, 4) + mathtools.NonreducedFraction(2, 8)
    assert isinstance(result, mathtools.NonreducedFraction)
    assert result.pair == (4, 8)

    result = mathtools.NonreducedFraction(2, 8) + Duration(1, 4)
    assert isinstance(result, mathtools.NonreducedFraction)
    assert result.pair == (4, 8)
