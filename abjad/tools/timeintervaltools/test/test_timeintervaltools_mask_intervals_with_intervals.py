# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_mask_intervals_with_intervals_01():
    time_interval_1 = TimeInterval(0, 9, {'time_interval_1': 1})
    time_interval_2 = TimeInterval(6, 10, {'time_interval_2': 2})
    time_interval_3 = TimeInterval(5, 10, {'time_interval_3': 3})
    masked = TimeIntervalTree([time_interval_1, time_interval_2])
    mask = TimeIntervalTree([time_interval_3])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 9), (6, 10)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures
    assert result[0]._data == time_interval_1._data
    assert result[1]._data == time_interval_2._data
#   assert result[0] == time_interval_1
#   assert result[1] == time_interval_2

def test_timeintervaltools_mask_intervals_with_intervals_02():
    time_interval_1 = TimeInterval(0, 9, {'time_interval_1': 1})
    time_interval_2 = TimeInterval(6, 10, {'time_interval_2': 2})
    time_interval_3 = TimeInterval(5, 6, {'time_interval_3': 3})
    time_interval_4 = TimeInterval(7, 8, {'time_interval_4': 4})
    masked = TimeIntervalTree([time_interval_1, time_interval_2])
    mask = TimeIntervalTree([time_interval_3, time_interval_4])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 6), (7, 8), (7, 8)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures

def test_timeintervaltools_mask_intervals_with_intervals_03():
    time_interval_1 = TimeInterval(0, 9, {'time_interval_1': 1})
    time_interval_2 = TimeInterval(6, 10, {'time_interval_2': 2})
    time_interval_3 = TimeInterval(11, 12, {'time_interval_3': 3})
    masked = TimeIntervalTree([time_interval_1, time_interval_2])
    mask = TimeIntervalTree([time_interval_3])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = []
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures

def test_timeintervaltools_mask_intervals_with_intervals_04():
    time_interval_1 = TimeInterval(0, 9, {'time_interval_1': 1})
    time_interval_2 = TimeInterval(6, 10, {'time_interval_2': 2})
    time_interval_3 = TimeInterval(7, 8, {'time_interval_3': 3})
    time_interval_4 = TimeInterval(11, 12, {'time_interval_4': 4})
    masked = TimeIntervalTree([time_interval_1, time_interval_2])
    mask = TimeIntervalTree([time_interval_3, time_interval_4])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(7, 8), (7, 8)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures
