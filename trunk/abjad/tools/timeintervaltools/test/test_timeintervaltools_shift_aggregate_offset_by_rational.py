from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_shift_aggregate_offset_by_rational_01():
    rational = 0
    tree = TimeIntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.duration == shifted.duration
    assert tree.start == shifted.start

def test_timeintervaltools_shift_aggregate_offset_by_rational_02():
    rational = Fraction(1, 2)
    tree = TimeIntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.duration == shifted.duration
    assert tree.start != shifted.start
    assert shifted.start == rational

def test_timeintervaltools_shift_aggregate_offset_by_rational_03():
    rational = Fraction(-1, 2)
    tree = TimeIntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.duration == shifted.duration
    assert tree.start != shifted.start
    assert shifted.start == rational

def test_timeintervaltools_shift_aggregate_offset_by_rational_04():
    rational = Fraction(-1, 2)
    tree = TimeIntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)
    shifted = shift_aggregate_offset_by_rational(shifted, rational)

    assert tree.duration == shifted.duration
    assert tree.start != shifted.start
    assert shifted.start == rational * 2
