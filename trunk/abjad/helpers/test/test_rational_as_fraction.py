from abjad.helpers.rational_as_fraction import _rational_as_fraction
from abjad import *


def test_rational_as_fraction_01( ):
   assert _rational_as_fraction(Rational(1)) == '1/1'
   assert _rational_as_fraction(Rational(1, 2)) == '1/2'
   assert _rational_as_fraction(Rational(1, 4)) == '1/4'
   assert _rational_as_fraction(Rational(2)) == '2/1'
   assert _rational_as_fraction(Rational(2, 2)) == '1/1'
   assert _rational_as_fraction(Rational(2, 4)) == '1/2'
   assert _rational_as_fraction(Rational(-3)) == '-3/1'
   assert _rational_as_fraction(Rational(-4)) == '-4/1'
