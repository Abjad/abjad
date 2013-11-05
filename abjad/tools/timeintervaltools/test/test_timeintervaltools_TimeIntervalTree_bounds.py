# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.timeintervaltools import TimeInterval
from abjad.tools.timeintervaltools import TimeIntervalTree


def test_timeintervaltools_TimeIntervalTree_bounds_01():
    tree = TimeIntervalTree([])
    pytest.raises(Exception, 'tree.bounds')

def test_timeintervaltools_TimeIntervalTree_bounds_02():
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    assert tree.bounds == TimeInterval(0, 37)
