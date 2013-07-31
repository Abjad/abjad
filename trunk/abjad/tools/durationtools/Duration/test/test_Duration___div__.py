# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.mathtools import NonreducedFraction


def test_Duration___div___01():
    r'''Dividing duration by nonreduced fraction gives nonreduced fraction.
    '''

    result = Duration(1) / NonreducedFraction(3, 3)
    assert isinstance(result, NonreducedFraction)
    assert result.pair == (3, 3)

    result = NonreducedFraction(3, 3) / Duration(1)
    assert isinstance(result, NonreducedFraction)
    assert result.pair == (3, 3)
