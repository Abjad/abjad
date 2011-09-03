from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_mask_intervals_with_intervals_01():
    a = BoundedInterval(0, 9, {'a': 1})
    b = BoundedInterval(6, 10, {'b': 2})
    c = BoundedInterval(5, 10, {'c': 3})
    masked = IntervalTree([a, b])
    mask = IntervalTree([c])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 9), (6, 10)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures
    assert dict.__eq__(result[0], a)
    assert dict.__eq__(result[1], b)
#   assert result[0] == a
#   assert result[1] == b

def test_intervaltreetools_mask_intervals_with_intervals_02():
    a = BoundedInterval(0, 9, {'a': 1})
    b = BoundedInterval(6, 10, {'b': 2})
    c = BoundedInterval(5, 6, {'c': 3})
    d = BoundedInterval(7, 8, {'d': 4})
    masked = IntervalTree([a, b])
    mask = IntervalTree([c, d])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 6), (7, 8), (7, 8)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures

def test_intervaltreetools_mask_intervals_with_intervals_03():
    a = BoundedInterval(0, 9, {'a': 1})
    b = BoundedInterval(6, 10, {'b': 2})
    c = BoundedInterval(11, 12, {'c': 3})
    masked = IntervalTree([a, b])
    mask = IntervalTree([c])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = []
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures

def test_intervaltreetools_mask_intervals_with_intervals_04():
    a = BoundedInterval(0, 9, {'a': 1})
    b = BoundedInterval(6, 10, {'b': 2})
    c = BoundedInterval(7, 8, {'c': 3})
    d = BoundedInterval(11, 12, {'d': 4})
    masked = IntervalTree([a, b])
    mask = IntervalTree([c, d])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(7, 8), (7, 8)]
    actual_signatures = [interval.signature for interval in result]
    assert target_signatures == actual_signatures
