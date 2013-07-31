# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_intervals_are_contiguous_01():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(10, 20)
    c = timeintervaltools.TimeInterval(20, 30)
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    assert tree.intervals_are_contiguous


def test_TimeIntervalTree_intervals_are_contiguous_02():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b])
    assert not tree.intervals_are_contiguous


def test_TimeIntervalTree_intervals_are_contiguous_03():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(15, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b])
    assert not tree.intervals_are_contiguous
