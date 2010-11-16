import py.test
from fractions import Fraction
from abjad.tools.treetools.BoundedInterval import BoundedInterval


def test_BoundedInterval_scale_to_value_01( ):
    '''BoundedInterval.scale_to_value returns a new BoundedInterval instance unless value is old magnitude.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_to_value(21)
    assert i1 != i2
    i2 = i1.scale_to_value(20)
    assert i1 == i2

def test_BoundedInterval_scale_to_value_02( ):
    '''BoundedInterval magnitudes can be scaled to int values.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_to_value(10)
    assert i1.low == i2.low
    assert i2.magnitude == 10

def test_BoundedInterval_scale_to_value_03( ):
    '''BoundedInterval magnitudes can be scaled to Fractional values.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_to_value(Fraction(2, 5))
    assert i1.low == i2.low
    assert i2.magnitude == Fraction(2, 5)

def test_BoundedInterval_scale_to_value_04( ):
    '''BoundedInterval magnitudes can be scaled to zero.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_to_value(0)
    assert i2.low == i2.high

def test_BoundedInterval_scale_to_value_05( ):
    '''BoundedInterval magnitudes cannot be scaled to negative values.'''
    i1 = BoundedInterval(3, 23)
    py.test.raises(AssertionError,
        'i2 = i1.scale_to_value(-1)')

