# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_TimeIntervalTree___eq___01():
    time_interval_1 = TimeIntervalTree(timeintervaltools.make_test_intervals())
    time_interval_2 = TimeIntervalTree(timeintervaltools.make_test_intervals())
    assert time_interval_1 == time_interval_2


def test_TimeIntervalTree___eq___02():
    time_interval_1 = TimeIntervalTree(timeintervaltools.make_test_intervals())
    time_interval_2 = TimeIntervalTree(timeintervaltools.make_test_intervals()[:-1])
    assert time_interval_1 != time_interval_2


def test_TimeIntervalTree___eq___03():
    time_interval_1 = TimeIntervalTree([])
    time_interval_2 = TimeIntervalTree([])
    assert time_interval_1 == time_interval_2
