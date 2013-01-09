from abjad import *


def test_Timespan_stops_when_timespan_stops_01():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, -5)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_02():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 0)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_03():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 5)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_04():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 15)
    assert a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_05():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 25)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_06():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 10)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_07():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 15)
    assert a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_08():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 10)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_09():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 15)
    assert a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_10():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 25)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_11():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 25)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_12():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(15, 25)
    assert not a.stops_when_timespan_stops(b)

def test_Timespan_stops_when_timespan_stops_13():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(20, 25)
    assert not a.stops_when_timespan_stops(b)


