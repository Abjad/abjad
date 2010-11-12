import py.test
from fractions import Fraction
from abjad.tools.treetools._Interval import _Interval


def test__Interval_scale_by_value_01( ):
    '''_Interval.scale_by_value returns a new _Interval instance unless value is 1.'''
    i1 = _Interval(3, 23)
    i2 = i1.scale_by_value(2)
    assert i1 != i2
    i2 = i1.scale_by_value(1)
    assert i1 == i2

def test__Interval_scale_by_value_02( ):
    '''_Interval magnitude can be scaled with ints.'''
    i1 = _Interval(3, 23)
    i2 = i1.scale_by_value(2)
    assert i2.low == 3
    assert i2.magnitude == 40

def test__Interval_scale_by_value_03( ):
    '''_Interval magnitude can be scaled with Fractions.'''
    i1 = _Interval(3, 23)
    i2 = i1.scale_by_value(Fraction(1, 2))
    assert i2.low == 3
    assert i2.magnitude == 10

def test__Interval_scale_by_value_04( ):
    '''_Interval magnitude can be scaled to zero.'''
    i1 = _Interval(3, 23)
    i2 = i1.scale_by_value(0)
    assert i2.magnitude == 0

def test__Interval_scale_by_value_05( ):
    '''_Interval magnitude cannot be scaled with negatives.'''
    i1 = _Interval(3, 23)
    py.test.raises(AssertionError,
        'i2 = i1.scale_by_value(-1)')
