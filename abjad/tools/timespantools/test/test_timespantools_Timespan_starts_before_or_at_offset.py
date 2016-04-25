# -*- coding: utf-8 -*-
from abjad import *


def test_timespantools_Timespan_starts_before_or_at_offset_01():
    timespan = timespantools.Timespan(0, 10)
    offset = durationtools.Offset(-5)
    assert not timespan.starts_before_or_at_offset(offset)

def test_timespantools_Timespan_starts_before_or_at_offset_02():
    timespan = timespantools.Timespan(0, 10)
    offset = durationtools.Offset(0)
    assert timespan.starts_before_or_at_offset(offset)

def test_timespantools_Timespan_starts_before_or_at_offset_03():
    timespan = timespantools.Timespan(0, 10)
    offset = durationtools.Offset(5)
    assert timespan.starts_before_or_at_offset(offset)

def test_timespantools_Timespan_starts_before_or_at_offset_04():
    timespan = timespantools.Timespan(0, 10)
    offset = durationtools.Offset(10)
    assert timespan.starts_before_or_at_offset(offset)

def test_timespantools_Timespan_starts_before_or_at_offset_05():
    timespan = timespantools.Timespan(0, 10)
    offset = durationtools.Offset(15)
    assert timespan.starts_before_or_at_offset(offset)
