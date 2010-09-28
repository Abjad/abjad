from abjad import *


def test_durtools_rational_to_equal_or_greater_binary_rational_01( ):
   '''Return least written duration of the form 1 / 2 ** n, such that
      written duration is greater than or equal to prolated duration.'''

   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(1, 80)) == Fraction(1, 64)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(2, 80)) == Fraction(1, 32)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(3, 80)) == Fraction(1, 16)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(4, 80)) == Fraction(1, 16)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(5, 80)) == Fraction(1, 16)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(6, 80)) == Fraction(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(7, 80)) == Fraction(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(8, 80)) == Fraction(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(9, 80)) == Fraction(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(10, 80)) == Fraction(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(11, 80)) == Fraction(1, 4)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Fraction(12, 80)) == Fraction(1, 4)
