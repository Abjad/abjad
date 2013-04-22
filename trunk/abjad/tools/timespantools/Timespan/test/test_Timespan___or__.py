from abjad import *


def test_Timespan___or___01():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, -5)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, -5),
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___or___02():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 0)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 15)
    ])

def test_Timespan___or___03():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 5)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 15)
    ])

def test_Timespan___or___04():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 15)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 15)
    ])

def test_Timespan___or___05():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 25)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 25)
    ])

def test_Timespan___or___06():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 10)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___or___07():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 15)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___or___08():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 10)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___or___09():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 15)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___or___10():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 25)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 25)
    ])

def test_Timespan___or___11():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 25)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 25)
    ])

def test_Timespan___or___12():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(15, 25)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 25)
    ])

def test_Timespan___or___13():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(20, 25)
    result = a | b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15),
        timespantools.Timespan(20, 25)
    ])
