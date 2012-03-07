from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals


def test_TimeIntervalTree___eq___01():
    a = TimeIntervalTree(_make_test_intervals())
    b = TimeIntervalTree(_make_test_intervals())
    assert a == b


def test_TimeIntervalTree___eq___02():
    a = TimeIntervalTree(_make_test_intervals())
    b = TimeIntervalTree(_make_test_intervals()[:-1])
    assert a != b


def test_TimeIntervalTree___eq___03():
    a = TimeIntervalTree([])
    b = TimeIntervalTree([])
    assert a == b
