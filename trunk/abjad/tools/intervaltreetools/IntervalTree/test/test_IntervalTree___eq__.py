from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_IntervalTree___eq___01():
    a = IntervalTree(_make_test_intervals())
    b = IntervalTree(_make_test_intervals())
    assert a == b


def test_IntervalTree___eq___02():
    a = IntervalTree(_make_test_intervals())
    b = IntervalTree(_make_test_intervals()[:-1])
    assert a != b


def test_IntervalTree___eq___03():
    a = IntervalTree([])
    b = IntervalTree([])
    assert a == b
