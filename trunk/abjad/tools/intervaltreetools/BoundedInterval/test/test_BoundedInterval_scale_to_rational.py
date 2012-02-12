from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad import Fraction
import py.test


def test_BoundedInterval_scale_to_rational_01():
    '''BoundedInterval.scale_to_rational returns a new BoundedInterval instance unless offset is old duration.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_to_rational(21)
    assert i1 != i2
    i2 = i1.scale_to_rational(20)
    assert i1 == i2

def test_BoundedInterval_scale_to_rational_02():
    '''BoundedInterval durations can be scaled to int offsets.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_to_rational(10)
    assert i1.start == i2.start
    assert i2.duration == 10

def test_BoundedInterval_scale_to_rational_03():
    '''BoundedInterval durations can be scaled to Fractional offsets.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_to_rational(Fraction(2, 5))
    assert i1.start == i2.start
    assert i2.duration == Fraction(2, 5)

def test_BoundedInterval_scale_to_rational_04():
    '''BoundedInterval durations cannot be scaled to zero.'''
    i1 = BoundedInterval(3, 23)
    py.test.raises(AssertionError,
        'i1.scale_to_rational(0)')

def test_BoundedInterval_scale_to_rational_05():
    '''BoundedInterval durations cannot be scaled to negative offsets.'''
    i1 = BoundedInterval(3, 23)
    py.test.raises(AssertionError,
        'i2 = i1.scale_to_rational(-1)')
