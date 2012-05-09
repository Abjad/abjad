from abjad import *
from abjad.tools.mathtools import NonreducedFraction


def test_durationtools_Duration___add___01():
    '''Adding two durations returns a third duration.
    '''

    duration = Duration(1, 2) + Duration(1, 3)
    assert isinstance(duration, Duration)


def test_durationtools_Duration___add___02():
    '''Adding a duration and nonreduced fraction returns a nonreduced fraction.
    '''
    
    result = Duration(1, 4) + NonreducedFraction(2, 8)
    assert isinstance(result, NonreducedFraction)
    assert result.pair == (4, 8)

    result = NonreducedFraction(2, 8) + Duration(1, 4)
    assert isinstance(result, NonreducedFraction)
    assert result.pair == (4, 8)
