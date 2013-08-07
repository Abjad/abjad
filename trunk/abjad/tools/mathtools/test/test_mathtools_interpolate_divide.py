# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_mathtools_interpolate_divide_01():
    r'''mathtools_interpolate_divide returns floats.
    '''

    t = mathtools.interpolate_divide(2, 1, 0.5)

    assert isinstance(t[0], float)


def test_mathtools_interpolate_divide_02():
    r'''mathtools_interpolate_divide can take Fractions and floats.
    '''

    fractions = mathtools.interpolate_divide(Fraction(1), Fraction(1, 2), 0.5)

    assert fractions == [0.5, 0.5]


def test_mathtools_interpolate_divide_03():
    r'''start_frac + stop_frac musb be < total.
    '''

    assert py.test.raises(ValueError, 't = mathtools.interpolate_divide(1, 2, 0.5)')
    assert py.test.raises(ValueError, 't = mathtools.interpolate_divide(1, 0.7, 0.5)')


def test_mathtools_interpolate_divide_04():
    r'''mathtools_interpolate_divide can go from larger to smaller divisions.
    '''

    fraction = mathtools.interpolate_divide(Fraction(1, 2), Fraction(1, 8), Fraction(1, 16))

    assert fraction[0] <= Fraction(1, 8) # 1/8 is approximated
    assert fraction[-2] < fraction[0]


def test_mathtools_interpolate_divide_05():
    r'''mathtools_interpolate_divide can go from smaller to larger divisions.
    '''

    fraction = mathtools.interpolate_divide(Fraction(1, 2), Fraction(1, 16), Fraction(1, 8))

    assert fraction[0] <= Fraction(1, 16) # 1/8 is approximated
    assert fraction[0] < fraction[-2]


def test_mathtools_interpolate_divide_06():
    r'''mathtools_interpolate_divide can take an exponent for exponential interpolation.
    '''

    t = mathtools.interpolate_divide(Fraction(1, 2), Fraction(1, 16), Fraction(1, 8), 2)

    assert t[0] <= Fraction(1, 16)
    assert t[0] < t[-2]
