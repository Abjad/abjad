from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_mask_intervals_with_intervals_01():
    a = TimeInterval(0, 9, {'a': 1})
    b = TimeInterval(6, 10, {'b': 2})
    c = TimeInterval(5, 10, {'c': 3})
    masked = TimeIntervalTree([a, b])
    mask = TimeIntervalTree([c])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 9), (6, 10)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures
    assert result[0]._data == a._data
    assert result[1]._data == b._data
#   assert result[0] == a
#   assert result[1] == b

def test_timeintervaltools_mask_intervals_with_intervals_02():
    a = TimeInterval(0, 9, {'a': 1})
    b = TimeInterval(6, 10, {'b': 2})
    c = TimeInterval(5, 6, {'c': 3})
    d = TimeInterval(7, 8, {'d': 4})
    masked = TimeIntervalTree([a, b])
    mask = TimeIntervalTree([c, d])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 6), (7, 8), (7, 8)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures

def test_timeintervaltools_mask_intervals_with_intervals_03():
    a = TimeInterval(0, 9, {'a': 1})
    b = TimeInterval(6, 10, {'b': 2})
    c = TimeInterval(11, 12, {'c': 3})
    masked = TimeIntervalTree([a, b])
    mask = TimeIntervalTree([c])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = []
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures

def test_timeintervaltools_mask_intervals_with_intervals_04():
    a = TimeInterval(0, 9, {'a': 1})
    b = TimeInterval(6, 10, {'b': 2})
    c = TimeInterval(7, 8, {'c': 3})
    d = TimeInterval(11, 12, {'d': 4})
    masked = TimeIntervalTree([a, b])
    mask = TimeIntervalTree([c, d])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(7, 8), (7, 8)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures
