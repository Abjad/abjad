# -*- coding: utf-8 -*-
from abjad import *


def test_durationtools_Duration___div___01():
    r'''Dividing duration by nonreduced fraction gives nonreduced fraction.
    '''

    result = Duration(1) / mathtools.NonreducedFraction(3, 3)
    assert isinstance(result, mathtools.NonreducedFraction)
    assert result.pair == (3, 3)

    result = mathtools.NonreducedFraction(3, 3) / Duration(1)
    assert isinstance(result, mathtools.NonreducedFraction)
    assert result.pair == (3, 3)
