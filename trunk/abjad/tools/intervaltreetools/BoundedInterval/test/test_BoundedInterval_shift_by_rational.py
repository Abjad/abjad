from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad import Fraction


def test_BoundedInterval_shift_by_rational_01():
    '''BoundedInterval.shift_by_rational returns a new BoundedInterval instance unless offset is zero.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_by_rational(1)
    assert i1 != i2
    i2 = i1.shift_by_rational(0)
    assert i1 == i2

def test_BoundedInterval_shift_by_rational_02():
    '''BoundedIntervals can be shifted by ints.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_by_rational(2)
    assert i2.low == 5
    assert i2.magnitude == i1.magnitude

def test_BoundedInterval_shift_by_rational_03():
    '''BoundedIntervals can be shifted by fractions.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_by_rational(Fraction(1, 5))
    assert i2.low == Fraction(16, 5)
    assert i2.magnitude == i1.magnitude
