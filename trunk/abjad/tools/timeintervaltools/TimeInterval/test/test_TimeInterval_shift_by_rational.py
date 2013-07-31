# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval


def test_TimeInterval_shift_by_rational_01():
    r'''TimeInterval.shift_by_rational returns a new TimeInterval instance unless offset is zero.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.shift_by_rational(1)
    assert i1 != i2
    i2 = i1.shift_by_rational(0)
    assert i1 == i2


def test_TimeInterval_shift_by_rational_02():
    r'''TimeIntervals can be shifted by ints.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.shift_by_rational(2)
    assert i2.start_offset == 5
    assert i2.duration == i1.duration


def test_TimeInterval_shift_by_rational_03():
    r'''TimeIntervals can be shifted by fractions.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.shift_by_rational(Fraction(1, 5))
    assert i2.start_offset == Fraction(16, 5)
    assert i2.duration == i1.duration
