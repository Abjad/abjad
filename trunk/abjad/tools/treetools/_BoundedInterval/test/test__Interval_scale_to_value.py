import py.test
from fractions import Fraction
from abjad.tools.treetools._BoundedInterval import _BoundedInterval


def test__BoundedInterval_scale_to_value_01( ):
    '''_BoundedInterval.scale_to_value returns a new _BoundedInterval instance unless value is old magnitude.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_to_value(21)
    assert i1 != i2
    i2 = i1.scale_to_value(20)
    assert i1 == i2

def test__BoundedInterval_scale_to_value_02( ):
    '''_BoundedInterval magnitudes can be scaled to int values.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_to_value(10)
    assert i1.low == i2.low
    assert i2.magnitude == 10

def test__BoundedInterval_scale_to_value_03( ):
    '''_BoundedInterval magnitudes can be scaled to Fractional values.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_to_value(Fraction(2, 5))
    assert i1.low == i2.low
    assert i2.magnitude == Fraction(2, 5)

def test__BoundedInterval_scale_to_value_04( ):
    '''_BoundedInterval magnitudes can be scaled to zero.'''
    i1 = _BoundedInterval(3, 23)
    i2 = i1.scale_to_value(0)
    assert i2.low == i2.high

def test__BoundedInterval_scale_to_value_05( ):
    '''_BoundedInterval magnitudes cannot be scaled to negative values.'''
    i1 = _BoundedInterval(3, 23)
    py.test.raises(AssertionError,
        'i2 = i1.scale_to_value(-1)')

