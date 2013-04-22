from abjad import *


def test_Timespan___xor___01():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, -5)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, -5),
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___xor___02():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 0)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 0),
        timespantools.Timespan(0, 15)
    ])

def test_Timespan___xor___03():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 5)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 0),
        timespantools.Timespan(5, 15)
    ])

def test_Timespan___xor___04():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 15)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 0)
    ])

def test_Timespan___xor___05():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(-10, 25)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(-10, 0),
        timespantools.Timespan(15, 25)
    ])

def test_Timespan___xor___06():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 10)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(10, 15)
    ])

def test_Timespan___xor___07():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 15)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
    ])

def test_Timespan___xor___08():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 10)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5),
        timespantools.Timespan(10, 15)
    ])

def test_Timespan___xor___09():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 15)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5)
    ])

def test_Timespan___xor___10():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(0, 25)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(15, 25)
    ])

def test_Timespan___xor___11():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(5, 25)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5),
        timespantools.Timespan(15, 25)
    ])

def test_Timespan___xor___12():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(15, 25)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15),
        timespantools.Timespan(15, 25)
    ])

def test_Timespan___xor___13():
    a = timespantools.Timespan(0, 15)
    b = timespantools.Timespan(20, 25)
    result = a ^ b
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15),
        timespantools.Timespan(20, 25)
    ])
