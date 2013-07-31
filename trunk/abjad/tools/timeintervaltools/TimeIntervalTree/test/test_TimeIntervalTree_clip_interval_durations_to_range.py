# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_clip_interval_durations_to_range_01():
    start_offset = None
    stop_offset = None
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = tree.clip_interval_durations_to_range(start_offset, stop_offset)
    assert clipped[:] == tree[:]
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_TimeIntervalTree_clip_interval_durations_to_range_02():
    start_offset = Fraction(3, 4)
    stop_offset = None
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = tree.clip_interval_durations_to_range(start_offset, stop_offset)
    assert all(start_offset <= x.duration for x in clipped)
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_TimeIntervalTree_clip_interval_durations_to_range_03():
    start_offset = None
    stop_offset = Fraction(1, 5)
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = tree.clip_interval_durations_to_range(start_offset, stop_offset)
    assert all(x.duration <= stop_offset for x in clipped)
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_TimeIntervalTree_clip_interval_durations_to_range_04():
    start_offset = Fraction(1, 7)
    stop_offset = Fraction(1, 3)
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    clipped = tree.clip_interval_durations_to_range(start_offset, stop_offset)
    assert all(start_offset <= x.duration <= stop_offset for x in clipped)
    assert sorted([x.start_offset for x in tree]) == sorted([x.start_offset for x in clipped])


def test_TimeIntervalTree_clip_interval_durations_to_range_05():
    start_offset = Fraction(1, 3)
    stop_offset = Fraction(1, 7)
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())
    py.test.raises(AssertionError, 
        "clipped = tree.clip_interval_durations_to_range(start_offset, stop_offset)")
