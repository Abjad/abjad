# -*- encoding: utf-8 -*-
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval


def test_timeintervaltools_TimeInterval_duration_01():
    r'''TimeInterval duration is the stop_offset minus the start_offset offset.
    '''

    time_interval = TimeInterval(3, 23)
    assert (23 - 3) == time_interval.duration
