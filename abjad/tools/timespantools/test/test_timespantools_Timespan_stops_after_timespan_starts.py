# -*- coding: utf-8 -*-
from abjad import *


def test_timespantools_Timespan_stops_after_timespan_starts_01():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, -5)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_02():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 0)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_03():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 5)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_04():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 15)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_05():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 25)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_06():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 10)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_07():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 15)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_08():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 10)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_09():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 15)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_10():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 25)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_11():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 25)
    assert timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_12():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(15, 25)
    assert not timespan_1.stops_after_timespan_starts(timespan_2)

def test_timespantools_Timespan_stops_after_timespan_starts_13():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(20, 25)
    assert not timespan_1.stops_after_timespan_starts(timespan_2)
