from abjad import *


def test_durtools_naive_prolated_to_written_not_less_than_01( ):
   '''Return least written duration of the form 1 / 2 ** n, such that
      written duration is greater than or equal to prolated duration.'''

   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(1, 80)) == Rational(1, 64)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(2, 80)) == Rational(1, 32)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(3, 80)) == Rational(1, 16)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(4, 80)) == Rational(1, 16)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(5, 80)) == Rational(1, 16)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(6, 80)) == Rational(1, 8)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(7, 80)) == Rational(1, 8)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(8, 80)) == Rational(1, 8)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(9, 80)) == Rational(1, 8)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(10, 80)) == Rational(1, 8)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(11, 80)) == Rational(1, 4)
   assert durtools.naive_prolated_to_written_not_less_than(
      Rational(12, 80)) == Rational(1, 4)
