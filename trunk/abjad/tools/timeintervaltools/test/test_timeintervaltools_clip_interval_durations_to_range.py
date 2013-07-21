from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_clip_interval_durations_to_range_01():
    start_offset = None
    stop_offset = None
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start_offset, stop_offset)
    assert clipped[:] == tree[:]
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_timeintervaltools_clip_interval_durations_to_range_02():
    start_offset = Fraction(3, 4)
    stop_offset = None
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start_offset, stop_offset)
    assert all(start_offset <= x.duration for x in clipped)
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_timeintervaltools_clip_interval_durations_to_range_03():
    start_offset = None
    stop_offset = Fraction(1, 5)
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start_offset, stop_offset)
    assert all(x.duration <= stop_offset for x in clipped)
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_timeintervaltools_clip_interval_durations_to_range_04():
    start_offset = Fraction(1, 7)
    stop_offset = Fraction(1, 3)
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = clip_interval_durations_to_range(tree, start_offset, stop_offset)
    assert all(start_offset <= x.duration <= stop_offset for x in clipped)
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_timeintervaltools_clip_interval_durations_to_range_05():
    start_offset = Fraction(1, 3)
    stop_offset = Fraction(1, 7)
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    py.test.raises(AssertionError, "clipped = clip_interval_durations_to_range(tree, start_offset, stop_offset)")
