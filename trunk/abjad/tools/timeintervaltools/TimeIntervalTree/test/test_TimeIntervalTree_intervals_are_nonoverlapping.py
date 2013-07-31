# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_TimeIntervalTree_intervals_are_nonoverlapping_01():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(10, 20)
    tree = timeintervaltools.TimeIntervalTree([a, b])
    assert tree.intervals_are_nonoverlapping


def test_TimeIntervalTree_intervals_are_nonoverlapping_02():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(5, 15)
    tree = timeintervaltools.TimeIntervalTree([a, b])
    assert not tree.intervals_are_nonoverlapping


def test_TimeIntervalTree_intervals_are_nonoverlapping_03():
    a = timeintervaltools.TimeInterval(0, 10)
    b = timeintervaltools.TimeInterval(15, 25)
    tree = timeintervaltools.TimeIntervalTree([a, b])
    assert tree.intervals_are_nonoverlapping
