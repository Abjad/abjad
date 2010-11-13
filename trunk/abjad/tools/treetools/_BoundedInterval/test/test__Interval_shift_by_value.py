from fractions import Fraction
from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval_shift_by_value_01( ):
    '''_BoundedInterval.shift_by_value returns a new _BoundedInterval instance unless value is zero.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.shift_by_value(1)
    assert i1 != i2
    i2 = i1.shift_by_value(0)
    assert i1 == i2

def test__BoundedInterval_shift_by_value_02( ):
    '''_BoundedIntervals can be shifted by ints.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.shift_by_value(2)
    assert i2.low == 5
    assert i2.magnitude == i1.magnitude

def test__BoundedInterval_shift_by_value_03( ):
    '''_BoundedIntervals can be shifted by fractions.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.shift_by_value(Fraction(1, 5))
    assert i2.low == Fraction(16, 5)
    assert i2.magnitude == i1.magnitude
