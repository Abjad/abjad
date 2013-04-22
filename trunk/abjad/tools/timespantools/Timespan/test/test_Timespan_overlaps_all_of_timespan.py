from abjad import *


def test_Timespan_overlaps_all_of_timespan_01():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, -5)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_02():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 0)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_03():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 5)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_04():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 15)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_05():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 25)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_06():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 10)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_07():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 15)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_08():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 10)
    assert a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_09():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 15)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_10():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 25)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_11():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 25)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_12():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(15, 25)
    assert not a.overlaps_all_of_timespan(b)

def test_Timespan_overlaps_all_of_timespan_13():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(20, 25)
    assert not a.overlaps_all_of_timespan(b)
