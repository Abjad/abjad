from abjad import *
import py.test


def test_mathtools_interpolate_divide_01( ):
   '''mathtools_interpolate_divide returns floats.'''

   t = mathtools.interpolate_divide(2, 1, 0.5)

   assert isinstance(t[0], float)


def test_mathtools_interpolate_divide_02( ):
   '''mathtools_interpolate_divide can take Rationals and floats.'''

   t = mathtools.interpolate_divide(Rational(1), Rational(1, 2), 0.5)

   assert t == [0.5, 0.5]


def test_mathtools_interpolate_divide_03( ):
   '''start_frac + stop_frac musb be < total.'''

   assert py.test.raises(ValueError, 't = mathtools.interpolate_divide(1, 2, 0.5)')
   assert py.test.raises(ValueError, 't = mathtools.interpolate_divide(1, 0.7, 0.5)')


def test_mathtools_interpolate_divide_04( ):
   '''mathtools_interpolate_divide can go from larger to smaller divisions.'''

   t = mathtools.interpolate_divide(Rational(1, 2), Rational(1, 8), Rational(1, 16))

   assert t[0] <= Rational(1, 8) ## 1/8 is approximated
   assert t[0] > t[-2]


def test_mathtools_interpolate_divide_05( ):
   '''mathtools_interpolate_divide can go from smaller to larger divisions.'''

   t = mathtools.interpolate_divide(Rational(1, 2), Rational(1, 16), Rational(1, 8))

   assert t[0] <= Rational(1, 16) ## 1/8 is approximated
   assert t[0] < t[-2]


def test_mathtools_interpolate_divide_06( ):
   '''mathtools_interpolate_divide can take an exponent for exponential interpolation.'''

   t = mathtools.interpolate_divide(Rational(1, 2), Rational(1, 16), Rational(1, 8), 2)

   assert t[0] <= Rational(1, 16)
   assert t[0] < t[-2]
