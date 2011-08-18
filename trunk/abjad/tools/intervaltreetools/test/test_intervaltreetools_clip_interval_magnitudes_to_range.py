from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_clip_interval_magnitudes_to_range_01():
    low = None
    high = None
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_magnitudes_to_range(tree, low, high)
    assert clipped[:] == tree[:]
    assert sorted([x.low for x in tree]) == sorted([x.low for x in clipped])


def test_intervaltreetools_clip_interval_magnitudes_to_range_02():
    low = Fraction(3, 4)
    high = None
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_magnitudes_to_range(tree, low, high)
    assert all([low <= x.magnitude for x in clipped])
    assert sorted([x.low for x in tree]) == sorted([x.low for x in clipped])


def test_intervaltreetools_clip_interval_magnitudes_to_range_03():
    low = None
    high = Fraction(1, 5)
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_magnitudes_to_range(tree, low, high)
    assert all([x.magnitude <= high for x in clipped])
    assert sorted([x.low for x in tree]) == sorted([x.low for x in clipped])


def test_intervaltreetools_clip_interval_magnitudes_to_range_04():
    low = Fraction(1, 7)
    high = Fraction(1, 3)
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_magnitudes_to_range(tree, low, high)
    assert all([low <= x.magnitude <= high for x in clipped])
    assert sorted([x.low for x in tree]) == sorted([x.low for x in clipped])


def test_intervaltreetools_clip_interval_magnitudes_to_range_05():
    low = Fraction(1, 3)
    high = Fraction(1, 7)
    tree = IntervalTree(_make_test_intervals())
    py.test.raises(AssertionError, "clipped = clip_interval_magnitudes_to_range(tree, low, high)")
