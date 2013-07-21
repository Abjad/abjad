from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_shift_aggregate_offset_by_rational_01():
    rational = 0
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.duration == shifted.duration
    assert tree.start_offset == shifted.start_offset

def test_timeintervaltools_shift_aggregate_offset_by_rational_02():
    rational = Fraction(1, 2)
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.duration == shifted.duration
    assert tree.start_offset != shifted.start_offset
    assert shifted.start_offset == rational

def test_timeintervaltools_shift_aggregate_offset_by_rational_03():
    rational = Fraction(-1, 2)
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.duration == shifted.duration
    assert tree.start_offset != shifted.start_offset
    assert shifted.start_offset == rational

def test_timeintervaltools_shift_aggregate_offset_by_rational_04():
    rational = Fraction(-1, 2)
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)
    shifted = shift_aggregate_offset_by_rational(shifted, rational)

    assert tree.duration == shifted.duration
    assert tree.start_offset != shifted.start_offset
    assert shifted.start_offset == rational * 2
