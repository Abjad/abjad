# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.mathtools import NonreducedFraction


def test_mathtools_NonreducedFraction___sub___01():

    result = NonreducedFraction(5, 4) - NonreducedFraction(18, 16)
    assert result.pair == (2, 16)

    result = NonreducedFraction(18, 16) - NonreducedFraction(5, 4)
    assert result.pair == (-2, 16)


def test_mathtools_NonreducedFraction___sub___02():

    result = NonreducedFraction(3, 3) - 2
    assert result.pair == (-3, 3)

    result = 2 - NonreducedFraction(3, 3)
    assert result.pair == (3, 3)
