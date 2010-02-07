from abjad import *
import py.test


def test_durtools_rational_to_dot_count_01( ):

   assert durtools.rational_to_dot_count(Rational(1, 16)) == 0
   assert durtools.rational_to_dot_count(Rational(2, 16)) == 0
   assert durtools.rational_to_dot_count(Rational(3, 16)) == 1
   assert durtools.rational_to_dot_count(Rational(4, 16)) == 0

   assert durtools.rational_to_dot_count(Rational(6, 16)) == 1
   assert durtools.rational_to_dot_count(Rational(7, 16)) == 2
   assert durtools.rational_to_dot_count(Rational(8, 16)) == 0


def test_durtools_rational_to_dot_count_02( ):

   assert py.test.raises(AssignabilityError, 
      'durtools.rational_to_dot_count(Rational(5, 16))')
