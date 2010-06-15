from abjad import *


def test_durtools_rational_to_equal_or_greater_binary_rational_01( ):
   '''Return least written duration of the form 1 / 2 ** n, such that
      written duration is greater than or equal to prolated duration.'''

   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(1, 80)) == Rational(1, 64)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(2, 80)) == Rational(1, 32)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(3, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(4, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(5, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(6, 80)) == Rational(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(7, 80)) == Rational(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(8, 80)) == Rational(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(9, 80)) == Rational(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(10, 80)) == Rational(1, 8)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(11, 80)) == Rational(1, 4)
   assert durtools.rational_to_equal_or_greater_binary_rational(
      Rational(12, 80)) == Rational(1, 4)
