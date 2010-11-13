import py.test
from fractions import Fraction
from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval_scale_by_value_01( ):
    '''_BoundedInterval.scale_by_value returns a new _BoundedInterval instance unless value is 1.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_by_value(2)
    assert i1 != i2
    i2 = i1.scale_by_value(1)
    assert i1 == i2

def test__BoundedInterval_scale_by_value_02( ):
    '''_BoundedInterval magnitude can be scaled with ints.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_by_value(2)
    assert i2.low == 3
    assert i2.magnitude == 40

def test__BoundedInterval_scale_by_value_03( ):
    '''_BoundedInterval magnitude can be scaled with Fractions.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_by_value(Fraction(1, 2))
    assert i2.low == 3
    assert i2.magnitude == 10

def test__BoundedInterval_scale_by_value_04( ):
    '''_BoundedInterval magnitude can be scaled to zero.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_by_value(0)
    assert i2.magnitude == 0

def test__BoundedInterval_scale_by_value_05( ):
    '''_BoundedInterval magnitude cannot be scaled with negatives.'''
    i1 = _BoundedInterval(3, 23)
    py.test.raises(AssertionError,
        'i2 = i1.scale_by_value(-1)')
