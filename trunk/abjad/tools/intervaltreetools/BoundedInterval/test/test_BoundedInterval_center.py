from abjad.tools.durationtools import Offset
from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_BoundedInterval_center_01():
    intervals = _make_test_intervals()
    for interval in intervals:
        assert interval.center == Offset(interval.start + interval.stop, 2)
