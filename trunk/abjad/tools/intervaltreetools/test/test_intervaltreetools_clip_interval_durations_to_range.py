from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_clip_interval_durations_to_range_01():
    start = None
    stop = None
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start, stop)
    assert clipped[:] == tree[:]
    assert sorted([x.start for x in tree]) == sorted([x.start for x in clipped])


def test_intervaltreetools_clip_interval_durations_to_range_02():
    start = Fraction(3, 4)
    stop = None
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start, stop)
    assert all([start <= x.duration for x in clipped])
    assert sorted([x.start for x in tree]) == sorted([x.start for x in clipped])


def test_intervaltreetools_clip_interval_durations_to_range_03():
    start = None
    stop = Fraction(1, 5)
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start, stop)
    assert all([x.duration <= stop for x in clipped])
    assert sorted([x.start for x in tree]) == sorted([x.start for x in clipped])


def test_intervaltreetools_clip_interval_durations_to_range_04():
    start = Fraction(1, 7)
    stop = Fraction(1, 3)
    tree = IntervalTree(_make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start, stop)
    assert all([start <= x.duration <= stop for x in clipped])
    assert sorted([x.start for x in tree]) == sorted([x.start for x in clipped])


def test_intervaltreetools_clip_interval_durations_to_range_05():
    start = Fraction(1, 3)
    stop = Fraction(1, 7)
    tree = IntervalTree(_make_test_intervals())
    py.test.raises(AssertionError, "clipped = clip_interval_durations_to_range(tree, start, stop)")
