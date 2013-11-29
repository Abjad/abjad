# -*- encoding: utf-8 -*-
from abjad import *


def test_timerelationtools_Timespan___xor___01():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, -5)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(-10, -5),
        timerelationtools.Timespan(0, 15)
    ])

def test_timerelationtools_Timespan___xor___02():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 0)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(-10, 0),
        timerelationtools.Timespan(0, 15)
    ])

def test_timerelationtools_Timespan___xor___03():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 5)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(-10, 0),
        timerelationtools.Timespan(5, 15)
    ])

def test_timerelationtools_Timespan___xor___04():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 15)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(-10, 0)
    ])

def test_timerelationtools_Timespan___xor___05():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 25)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(-10, 0),
        timerelationtools.Timespan(15, 25)
    ])

def test_timerelationtools_Timespan___xor___06():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(0, 10)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(10, 15)
    ])

def test_timerelationtools_Timespan___xor___07():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(0, 15)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
    ])

def test_timerelationtools_Timespan___xor___08():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(5, 10)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 5),
        timerelationtools.Timespan(10, 15)
    ])

def test_timerelationtools_Timespan___xor___09():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(5, 15)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 5)
    ])

def test_timerelationtools_Timespan___xor___10():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(0, 25)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(15, 25)
    ])

def test_timerelationtools_Timespan___xor___11():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(5, 25)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 5),
        timerelationtools.Timespan(15, 25)
    ])

def test_timerelationtools_Timespan___xor___12():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(15, 25)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 15),
        timerelationtools.Timespan(15, 25)
    ])

def test_timerelationtools_Timespan___xor___13():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(20, 25)
    result = timespan_1 ^ timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 15),
        timerelationtools.Timespan(20, 25)
    ])
