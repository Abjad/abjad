from abjad import *


def test_durtools_Duration___add___01():
    '''Adding two durations returns a third duration.
    '''

    duration = Duration(1, 2) + Duration(1, 3)
    assert isinstance(duration, Duration)
