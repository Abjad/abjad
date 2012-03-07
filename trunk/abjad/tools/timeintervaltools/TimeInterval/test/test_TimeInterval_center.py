from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeInterval_center_01():
    intervals = _make_test_intervals()
    for interval in intervals:
        assert interval.center == Offset(interval.start + interval.stop, 2)
