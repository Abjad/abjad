from abjad import *
import py.test


def test_durtools_assignable_rational_to_dot_count_01( ):

   assert durtools.assignable_rational_to_dot_count(Fraction(1, 16)) == 0
   assert durtools.assignable_rational_to_dot_count(Fraction(2, 16)) == 0
   assert durtools.assignable_rational_to_dot_count(Fraction(3, 16)) == 1
   assert durtools.assignable_rational_to_dot_count(Fraction(4, 16)) == 0

   assert durtools.assignable_rational_to_dot_count(Fraction(6, 16)) == 1
   assert durtools.assignable_rational_to_dot_count(Fraction(7, 16)) == 2
   assert durtools.assignable_rational_to_dot_count(Fraction(8, 16)) == 0


def test_durtools_assignable_rational_to_dot_count_02( ):

   assert py.test.raises(AssignabilityError, 
      'durtools.assignable_rational_to_dot_count(Fraction(5, 16))')
