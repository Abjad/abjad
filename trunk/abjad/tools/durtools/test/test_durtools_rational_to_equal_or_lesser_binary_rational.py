from abjad import *


def test_durtools_rational_to_equal_or_lesser_binary_rational_01( ):
   '''Return greatest written duration of the form 1 / 2 ** n, such that
   written duration is less than or equal to prolated duration.
   '''

   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(1, 80)) == Rational(1, 128)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(2, 80)) == Rational(1, 64)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(3, 80)) == Rational(1, 32)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(4, 80)) == Rational(1, 32)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(5, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(6, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(7, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(8, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(9, 80)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(10, 80)) == Rational(1, 8)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(11, 80)) == Rational(1, 8)
   assert durtools.rational_to_equal_or_lesser_binary_rational(
      Rational(12, 80)) == Rational(1, 8)


def test_durtools_rational_to_equal_or_lesser_binary_rational_02( ):
   '''Return greatest written duration of the form 1 / 2 ** n, such that
   written duration is less than or equal to prolated duration.
   '''

   assert durtools.rational_to_equal_or_lesser_binary_rational(Rational(1, 1)) == Rational(1, 1)
   assert durtools.rational_to_equal_or_lesser_binary_rational(Rational(3, 2)) == Rational(1, 1)

   assert durtools.rational_to_equal_or_lesser_binary_rational(Rational(2, 1)) == Rational(2, 1)
   assert durtools.rational_to_equal_or_lesser_binary_rational(Rational(3, 1)) == Rational(2, 1)

   assert durtools.rational_to_equal_or_lesser_binary_rational(Rational(4, 1)) == Rational(4, 1)
   assert durtools.rational_to_equal_or_lesser_binary_rational(Rational(5, 1)) == Rational(4, 1)
