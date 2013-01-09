from abjad import *


def test_Timespan_contains_timespan_improperly_01():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, -5)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_02():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 0)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_03():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 5)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_04():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 15)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_05():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 25)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_06():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 10)
    assert a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_07():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 15)
    assert a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_08():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 10)
    assert a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_09():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 15)
    assert a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_10():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 25)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_11():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 25)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_12():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(15, 25)
    assert not a.contains_timespan_improperly(b)

def test_Timespan_contains_timespan_improperly_13():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(20, 25)
    assert not a.contains_timespan_improperly(b)


