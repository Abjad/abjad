from abjad import *


def test_durtools_rational_to_prolation_string_01( ):

   assert durtools.rational_to_prolation_string(Rational(1, 1)) == '1:1'
   assert durtools.rational_to_prolation_string(Rational(1, 2)) == '2:1'
   assert durtools.rational_to_prolation_string(Rational(2, 2)) == '1:1'
   assert durtools.rational_to_prolation_string(Rational(1, 3)) == '3:1'
   assert durtools.rational_to_prolation_string(Rational(2, 3)) == '3:2'
   assert durtools.rational_to_prolation_string(Rational(3, 3)) == '1:1'
   assert durtools.rational_to_prolation_string(Rational(1, 4)) == '4:1'
   assert durtools.rational_to_prolation_string(Rational(2, 4)) == '2:1'
   assert durtools.rational_to_prolation_string(Rational(3, 4)) == '4:3'
   assert durtools.rational_to_prolation_string(Rational(4, 4)) == '1:1'
