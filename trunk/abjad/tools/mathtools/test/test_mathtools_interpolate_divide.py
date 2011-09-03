from abjad import *
from abjad.tools import mathtools
from fractions import Fraction
import py.test


def test_mathtools_interpolate_divide_01():
    '''mathtools_interpolate_divide returns floats.'''

    t = mathtools.interpolate_divide(2, 1, 0.5)

    assert isinstance(t[0], float)


def test_mathtools_interpolate_divide_02():
    '''mathtools_interpolate_divide can take Fractions and floats.'''

    t = mathtools.interpolate_divide(Fraction(1), Fraction(1, 2), 0.5)

    assert t == [0.5, 0.5]


def test_mathtools_interpolate_divide_03():
    '''start_frac + stop_frac musb be < total.'''

    assert py.test.raises(ValueError, 't = mathtools.interpolate_divide(1, 2, 0.5)')
    assert py.test.raises(ValueError, 't = mathtools.interpolate_divide(1, 0.7, 0.5)')


def test_mathtools_interpolate_divide_04():
    '''mathtools_interpolate_divide can go from larger to smaller divisions.'''

    t = mathtools.interpolate_divide(Fraction(1, 2), Fraction(1, 8), Fraction(1, 16))

    assert t[0] <= Fraction(1, 8) # 1/8 is approximated
    assert t[-2] < t[0]


def test_mathtools_interpolate_divide_05():
    '''mathtools_interpolate_divide can go from smaller to larger divisions.'''

    t = mathtools.interpolate_divide(Fraction(1, 2), Fraction(1, 16), Fraction(1, 8))

    assert t[0] <= Fraction(1, 16) # 1/8 is approximated
    assert t[0] < t[-2]


def test_mathtools_interpolate_divide_06():
    '''mathtools_interpolate_divide can take an exponent for exponential interpolation.'''

    t = mathtools.interpolate_divide(Fraction(1, 2), Fraction(1, 16), Fraction(1, 8), 2)

    assert t[0] <= Fraction(1, 16)
    assert t[0] < t[-2]
