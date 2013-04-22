from abjad import *


def test_Timespan_starts_before_timespan_starts_01():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, -5)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_02():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 0)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_03():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 5)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_04():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 15)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_05():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 25)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_06():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 10)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_07():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 15)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_08():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 10)
    assert a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_09():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 15)
    assert a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_10():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 25)
    assert not a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_11():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 25)
    assert a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_12():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(15, 25)
    assert a.starts_before_timespan_starts(b)

def test_Timespan_starts_before_timespan_starts_13():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(20, 25)
    assert a.starts_before_timespan_starts(b)
