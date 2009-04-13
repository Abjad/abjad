from abjad import *
import py.test


def test_interpolate_divide_01( ):
   '''interpolate_divide returns Rationals.'''
   t = interpolate.divide(2, 1, 0.5)
   assert isinstance(t[0], Rational)


def test_interpolate_divide_02( ):
   '''interpolate_divide can take Rationals and floats.'''
   t = interpolate.divide(Rational(1), Rational(1, 2), 0.5)
   assert t == [Rational(1, 2), Rational(1, 2)]


def test_interpolate_divide_03( ):
   '''start_frac and stop_frac musb be < total.'''
   assert py.test.raises(ValueError, 't = interpolate.divide(1, 2, 0.5)')


def test_interpolate_divide_04( ):
   '''interpolate_divide can go from larger to smaller divisions.'''
   t = interpolate.divide(Rational(1, 2), Rational(1, 8), Rational(1, 16))
   assert t[0] == Rational(1, 8)
   assert t[0] > t[-2]


def test_interpolate_divide_05( ):
   '''interpolate_divide can go from smaller to larger divisions.'''
   t = interpolate.divide(Rational(1, 2), Rational(1, 16), Rational(1, 8))
   assert t[0] == Rational(1, 16)
   assert t[0] < t[-2]


def test_interpolate_divide_06( ):
   '''interpolate_divide can take an exponent for exponential interpolation.'''
   t = interpolate.divide(Rational(1, 2), Rational(1, 16), Rational(1, 8), 2)
   assert t[0] == Rational(1, 16)
   assert t[0] < t[-2]
