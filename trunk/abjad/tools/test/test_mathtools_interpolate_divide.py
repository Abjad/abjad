from abjad.tools.mathtools import interpolate_divide
from abjad.rational.rational import Rational


def test_mathtools_interpolate_divide_01( ):
   '''interpolate_divide returns Rationals.'''
   t = interpolate_divide(1, 2, 0.5)
   assert isinstance(t[0], Rational)
   assert t == [1]


def test_mathtools_interpolate_divide_02( ):
   '''interpolate_divide can take Rationals and floats.'''
   t = interpolate_divide(Rational(1), Rational(1, 2), 0.5)
   assert t == [Rational(1, 2), Rational(1, 2)]


def test_mathtools_interpolate_divide_03( ):
   '''interpolate_divide returns the total interval if start_frac > total.'''
   t = interpolate_divide(1, 2, 0.5)
   assert t == [1]


def test_mathtools_interpolate_divide_04( ):
   '''interpolate_divide can go from larger to smaller divisions.'''
   t = interpolate_divide(Rational(1, 2), Rational(1, 8), Rational(1, 16))
   assert t[0] == Rational(1, 8)
   assert t[0] > t[-2]


def test_mathtools_interpolate_divide_05( ):
   '''interpolate_divide can go from smaller to larger divisions.'''
   t = interpolate_divide(Rational(1, 2), Rational(1, 16), Rational(1, 8))
   assert t[0] == Rational(1, 16)
   assert t[0] < t[-2]


def test_mathtools_interpolate_divide_06( ):
   '''interpolate_divide can take an exponent for exponential interpolation.'''
   t = interpolate_divide(Rational(1, 2), Rational(1, 16), Rational(1, 8), 2)
   assert t[0] == Rational(1, 16)
   assert t[0] < t[-2]


