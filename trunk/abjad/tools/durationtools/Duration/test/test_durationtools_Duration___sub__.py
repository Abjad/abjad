from abjad import *
from abjad.tools.mathtools import NonreducedFraction


def test_durationtools_Duration___sub___01():
    '''Subtracting nonreduced fraction from duration returns nonreduced fraction.
    '''

    result = Duration(1, 2) - NonreducedFraction(2, 8)
    assert isinstance(result, NonreducedFraction)
    assert result.pair == (2, 8)


def test_durationtools_Duration___sub___02():
    '''Subtracting duration from nonreduced fraction returns nonreduced fraction.
    '''

    result = NonreducedFraction(4, 8) - Duration(1, 4)
    assert isinstance(result, NonreducedFraction)
    assert result.pair == (2, 8)
