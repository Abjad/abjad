from abjad import *
from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools import *


def test_TimeInterval_center_01():
    intervals = timeintervaltools.make_test_intervals()
    for interval in intervals:
        assert interval.center == Offset(interval.start + interval.stop, 2)
