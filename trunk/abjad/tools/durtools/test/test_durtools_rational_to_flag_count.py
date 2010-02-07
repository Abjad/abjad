from abjad import *


def test_durtools_rational_to_flag_count_01( ):

   assert durtools.rational_to_flag_count(Rational(1, 64)) == 4
   assert durtools.rational_to_flag_count(Rational(2, 64)) == 3
   assert durtools.rational_to_flag_count(Rational(3, 64)) == 3
   assert durtools.rational_to_flag_count(Rational(4, 64)) == 2
   assert durtools.rational_to_flag_count(Rational(5, 64)) == 2
   assert durtools.rational_to_flag_count(Rational(6, 64)) == 2
   assert durtools.rational_to_flag_count(Rational(7, 64)) == 2
   assert durtools.rational_to_flag_count(Rational(8, 64)) == 1
