from abjad import *


def test_Timespan___sub___01():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, -5)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___sub___02():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 0)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___sub___03():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 5)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(5, 15)
    ])

def test_Timespan___sub___04():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 15)
    result = a - b
    assert result == timespantools.TimespanInventory([])

def test_Timespan___sub___05():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 25)
    result = a - b
    assert result == timespantools.TimespanInventory([])

def test_Timespan___sub___06():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 10)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(10, 15)
    ])

def test_Timespan___sub___07():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 15)
    result = a - b
    assert result == timespantools.TimespanInventory([])

def test_Timespan___sub___08():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 10)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5),
        timespantools.Timespan(10, 15)
    ])

def test_Timespan___sub___09():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 15)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5)
    ])

def test_Timespan___sub___10():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 25)
    result = a - b
    assert result == timespantools.TimespanInventory([])

def test_Timespan___sub___11():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 25)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5),
    ])

def test_Timespan___sub___12():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(15, 25)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15),
    ])

def test_Timespan___sub___13():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(20, 25)
    result = a - b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15),
    ])
