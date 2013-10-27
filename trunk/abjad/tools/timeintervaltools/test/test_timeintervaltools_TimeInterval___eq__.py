# -*- encoding: utf-8 -*-
from abjad.tools.timeintervaltools import TimeInterval


def test_timeintervaltools_TimeInterval___eq___01():
    time_interval_1 = TimeInterval(0, 10)
    time_interval_2 = TimeInterval(0, 10)
    assert time_interval_1 == time_interval_2


def test_timeintervaltools_TimeInterval___eq___02():
    time_interval_1 = TimeInterval(0, 10)
    time_interval_2 = TimeInterval(-1, 10)
    assert time_interval_1 != time_interval_2


def test_timeintervaltools_TimeInterval___eq___03():
    time_interval_1 = TimeInterval(0, 10)
    time_interval_2 = TimeInterval(0, 11)
    assert time_interval_1 != time_interval_2


def test_timeintervaltools_TimeInterval___eq___04():
    time_interval_1 = TimeInterval(0, 10)
    time_interval_2 = TimeInterval(0, 10, {})
    assert time_interval_1 == time_interval_2


def test_timeintervaltools_TimeInterval___eq___05():
    time_interval_1 = TimeInterval(0, 10, {'animal': 'goose'})
    time_interval_2 = TimeInterval(0, 10, {'animal': 'duck'})
    assert time_interval_1 != time_interval_2
