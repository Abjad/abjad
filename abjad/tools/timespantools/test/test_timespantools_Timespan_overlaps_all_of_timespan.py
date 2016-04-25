# -*- coding: utf-8 -*-
from abjad import *


def test_timespantools_Timespan_overlaps_all_of_timespan_01():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, -5)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_02():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 0)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_03():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 5)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_04():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 15)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_05():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 25)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_06():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 10)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_07():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 15)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_08():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 10)
    assert timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_09():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 15)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_10():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 25)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_11():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 25)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_12():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(15, 25)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)

def test_timespantools_Timespan_overlaps_all_of_timespan_13():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(20, 25)
    assert not timespan_1.overlaps_all_of_timespan(timespan_2)
