from abjad import *
from abjad.tools.timeintervaltools import *


def test_TimeIntervalTree___eq___01():
    a = TimeIntervalTree(timeintervaltools.make_test_intervals())
    b = TimeIntervalTree(timeintervaltools.make_test_intervals())
    assert a == b


def test_TimeIntervalTree___eq___02():
    a = TimeIntervalTree(timeintervaltools.make_test_intervals())
    b = TimeIntervalTree(timeintervaltools.make_test_intervals()[:-1])
    assert a != b


def test_TimeIntervalTree___eq___03():
    a = TimeIntervalTree([])
    b = TimeIntervalTree([])
    assert a == b
