from abjad import *


def test_durtools_rational_to_fraction_string_01( ):

   assert durtools.rational_to_fraction_string(Rational(1)) == '1/1'
   assert durtools.rational_to_fraction_string(Rational(1, 2)) == '1/2'
   assert durtools.rational_to_fraction_string(Rational(1, 4)) == '1/4'
   assert durtools.rational_to_fraction_string(Rational(2)) == '2/1'
   assert durtools.rational_to_fraction_string(Rational(2, 2)) == '1/1'
   assert durtools.rational_to_fraction_string(Rational(2, 4)) == '1/2'
   assert durtools.rational_to_fraction_string(Rational(-3)) == '-3/1'
   assert durtools.rational_to_fraction_string(Rational(-4)) == '-4/1'
