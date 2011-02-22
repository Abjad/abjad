from fractions import Fraction
from abjad.tools.treetools.BoundedInterval import BoundedInterval


def test_BoundedInterval_shift_by_offset_01( ):
    '''BoundedInterval.shift_by_offset returns a new BoundedInterval instance unless offset is zero.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_by_offset(1)
    assert i1 != i2
    i2 = i1.shift_by_offset(0)
    assert i1 == i2

def test_BoundedInterval_shift_by_offset_02( ):
    '''BoundedIntervals can be shifted by ints.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_by_offset(2)
    assert i2.low == 5
    assert i2.magnitude == i1.magnitude

def test_BoundedInterval_shift_by_offset_03( ):
    '''BoundedIntervals can be shifted by fractions.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.shift_by_offset(Fraction(1, 5))
    assert i2.low == Fraction(16, 5)
    assert i2.magnitude == i1.magnitude
