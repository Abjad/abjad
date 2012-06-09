from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from fractions import Fraction


def test_TimeInterval_shift_to_rational_01():
    '''TimeInterval.shift_to_rational returns a new TimeInterval instance unless offset is old start offset.'''
    i1 = TimeInterval(3, 23)
    i2 = i1.shift_to_rational(-1000)
    assert i1 != i2
    i2 = i1.shift_to_rational(3)
    assert i1 == i2

def test_TimeInterval_shift_to_rational_02():
    '''TimeIntervals can be shifted by ints.'''
    i1 = TimeInterval(3, 23)
    i2 = i1.shift_to_rational(-1)
    assert i2.start == -1
    assert i2.duration == i1.duration

def test_TimeInterval_shift_to_rational_03():
    '''TimeIntervals can be shifted by Fractions.'''
    i1 = TimeInterval(3, 23)
    i2 = i1.shift_to_rational(Fraction(-51, 3))
    assert i2.start == Fraction(-51, 3)
    assert i2.duration == i1.duration
