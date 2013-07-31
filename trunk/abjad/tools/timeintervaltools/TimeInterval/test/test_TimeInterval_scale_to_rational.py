# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
import py.test


def test_TimeInterval_scale_to_rational_01():
    r'''TimeInterval.scale_to_rational returns a new TimeInterval instance
    unless offset is old duration.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.scale_to_rational(21)
    assert i1 != i2
    i2 = i1.scale_to_rational(20)
    assert i1 == i2


def test_TimeInterval_scale_to_rational_02():
    r'''TimeInterval durations can be scaled to int offsets.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.scale_to_rational(10)
    assert i1.start_offset == i2.start_offset
    assert i2.duration == 10


def test_TimeInterval_scale_to_rational_03():
    r'''TimeInterval durations can be scaled to Fractional offsets.
    '''

    i1 = TimeInterval(3, 23)
    i2 = i1.scale_to_rational(Fraction(2, 5))
    assert i1.start_offset == i2.start_offset
    assert i2.duration == Fraction(2, 5)


def test_TimeInterval_scale_to_rational_04():
    r'''TimeInterval durations cannot be scaled to zero.
    '''

    i1 = TimeInterval(3, 23)
    py.test.raises(AssertionError,
        'i1.scale_to_rational(0)')


def test_TimeInterval_scale_to_rational_05():
    r'''TimeInterval durations cannot be scaled to negative offsets.
    '''

    i1 = TimeInterval(3, 23)
    py.test.raises(AssertionError,
        'i2 = i1.scale_to_rational(-1)')
