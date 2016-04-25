# -*- coding: utf-8 -*-
from abjad import *


def test_timespantools_Timespan___sub___01():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, -5)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_timespantools_Timespan___sub___02():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 0)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15)
    ])

def test_timespantools_Timespan___sub___03():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 5)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(5, 15)
    ])

def test_timespantools_Timespan___sub___04():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 15)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([])

def test_timespantools_Timespan___sub___05():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(-10, 25)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([])

def test_timespantools_Timespan___sub___06():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 10)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(10, 15)
    ])

def test_timespantools_Timespan___sub___07():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 15)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([])

def test_timespantools_Timespan___sub___08():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 10)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5),
        timespantools.Timespan(10, 15)
    ])

def test_timespantools_Timespan___sub___09():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 15)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5)
    ])

def test_timespantools_Timespan___sub___10():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(0, 25)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([])

def test_timespantools_Timespan___sub___11():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(5, 25)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 5),
    ])

def test_timespantools_Timespan___sub___12():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(15, 25)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15),
    ])

def test_timespantools_Timespan___sub___13():
    timespan_1 = timespantools.Timespan(0, 15)
    timespan_2 = timespantools.Timespan(20, 25)
    result = timespan_1 - timespan_2
    assert result == timespantools.TimespanInventory([
        timespantools.Timespan(0, 15),
    ])
