from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad import Fraction


def test_BoundedInterval_shift_to_rational_01():
    '''BoundedInterval.shift_to_rational returns a new BoundedInterval instance unless offset is old start offset.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_to_rational(-1000)
    assert i1 != i2
    i2 = i1.shift_to_rational(3)
    assert i1 == i2

def test_BoundedInterval_shift_to_rational_02():
    '''BoundedIntervals can be shifted by ints.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_to_rational(-1)
    assert i2.start == -1
    assert i2.duration == i1.duration

def test_BoundedInterval_shift_to_rational_03():
    '''BoundedIntervals can be shifted by Fractions.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_to_rational(Fraction(-51, 3))
    assert i2.start == Fraction(-51, 3)
    assert i2.duration == i1.duration
