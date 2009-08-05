from abjad import *


def test_durtools_to_fraction_01( ):
   assert durtools.to_fraction(Rational(1)) == '1/1'
   assert durtools.to_fraction(Rational(1, 2)) == '1/2'
   assert durtools.to_fraction(Rational(1, 4)) == '1/4'
   assert durtools.to_fraction(Rational(2)) == '2/1'
   assert durtools.to_fraction(Rational(2, 2)) == '1/1'
   assert durtools.to_fraction(Rational(2, 4)) == '1/2'
   assert durtools.to_fraction(Rational(-3)) == '-3/1'
   assert durtools.to_fraction(Rational(-4)) == '-4/1'
