# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_timeintervaltools_TimeIntervalTree_shift_to_rational_01():

    t1 = timeintervaltools.TimeInterval(-1, 3)
    t2 = timeintervaltools.TimeInterval(0, 1)
    t3 = timeintervaltools.TimeInterval(1, 2)

    tree = timeintervaltools.TimeIntervalTree([t1, t2, t3])
    offset = Offset(10, 1)
    result = tree.shift_to_rational(offset)

    assert type(result) == type(tree)
    assert result.duration == tree.duration
    assert [x.signature for x in result] == [
        (Offset(10, 1), Offset(14, 1)),
        (Offset(11, 1), Offset(12, 1)),
        (Offset(12, 1), Offset(13, 1))]


def test_timeintervaltools_TimeIntervalTree_shift_to_rational_02():
    rational = 0
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = tree.shift_to_rational(rational)

    assert tree.start_offset == 0
    assert tree.duration == shifted.duration
    assert tree.start_offset == shifted.start_offset


def test_timeintervaltools_TimeIntervalTree_shift_to_rational_03():
    rational = Fraction(1, 2)
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = tree.shift_to_rational(rational)

    assert tree.duration == shifted.duration
    assert tree.start_offset != shifted.start_offset
    assert shifted.start_offset == rational


def test_timeintervaltools_TimeIntervalTree_shift_to_rational_04():
    rational = Fraction(-1, 2)
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = tree.shift_to_rational(rational)

    assert tree.duration == shifted.duration
    assert tree.start_offset != shifted.start_offset
    assert shifted.start_offset == rational


def test_timeintervaltools_TimeIntervalTree_shift_to_rational_05():
    rational = Fraction(-1, 2)
    tree = timeintervaltools.TimeIntervalTree(timeintervaltools.make_test_intervals())

    shifted = tree.shift_to_rational(rational)
    shifted = shifted.shift_by_rational(-1 * rational)

    assert tree.duration == shifted.duration
    assert tree.start_offset == shifted.start_offset
