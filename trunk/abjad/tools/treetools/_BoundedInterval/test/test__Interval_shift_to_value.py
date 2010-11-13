from fractions import Fraction
from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval_shift_to_value_01( ):
    '''_BoundedInterval.shift_to_value returns a new _BoundedInterval instance unless value is old low value.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.shift_to_value(-1000)
    assert i1 != i2
    i2 = i1.shift_to_value(3)
    assert i1 == i2

def test__BoundedInterval_shift_to_value_02( ):
    '''_BoundedIntervals can be shifted by ints.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.shift_to_value(-1)
    assert i2.low == -1
    assert i2.magnitude == i1.magnitude

def test__BoundedInterval_shift_to_value_03( ):
    '''_BoundedIntervals can be shifted by Fractions.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.shift_to_value(Fraction(-51, 3))
    assert i2.low == Fraction(-51, 3)
    assert i2.magnitude == i1.magnitude
