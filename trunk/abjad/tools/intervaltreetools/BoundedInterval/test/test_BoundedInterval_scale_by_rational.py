from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad import Fraction
import py.test


def test_BoundedInterval_scale_by_rational_01():
    '''BoundedInterval.scale_by_rational returns a new BoundedInterval instance unless offset is 1.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_by_rational(2)
    assert i1 != i2
    i2 = i1.scale_by_rational(1)
    assert i1 == i2

def test_BoundedInterval_scale_by_rational_02():
    '''BoundedInterval magnitude can be scaled with ints.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_by_rational(2)
    assert i2.low == 3
    assert i2.magnitude == 40

def test_BoundedInterval_scale_by_rational_03():
    '''BoundedInterval magnitude can be scaled with Fractions.'''
    i1 = BoundedInterval(3, 23)
    i2 = i1.scale_by_rational(Fraction(1, 2))
    assert i2.low == 3
    assert i2.magnitude == 10

def test_BoundedInterval_scale_by_rational_04():
    '''BoundedInterval magnitude cannot be scaled to zero.'''
    i1 = BoundedInterval(3, 23)
    assert py.test.raises(AssertionError,
        'i1.scale_by_rational(0)')

def test_BoundedInterval_scale_by_rational_05():
    '''BoundedInterval magnitude cannot be scaled with negatives.'''
    i1 = BoundedInterval(3, 23)
    assert py.test.raises(AssertionError,
        'i2 = i1.scale_by_rational(-1)')
