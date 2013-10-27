# -*- encoding: utf-8 -*-
from abjad import *


def test_timespantools_Timespan_contains_timespan_improperly_01():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, -5)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_02():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 0)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_03():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 5)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_04():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 15)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_05():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 25)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_06():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 10)
    assert timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_07():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 15)
    assert timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_08():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 10)
    assert timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_09():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 15)
    assert timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_10():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 25)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_11():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 25)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_12():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(15, 25)
    assert not timespan_1.contains_timespan_improperly(timespan_2)

def test_timespantools_Timespan_contains_timespan_improperly_13():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(20, 25)
    assert not timespan_1.contains_timespan_improperly(timespan_2)
