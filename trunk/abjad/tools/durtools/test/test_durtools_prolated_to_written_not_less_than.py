from abjad import *


def test_durtools_prolated_to_written_not_less_than_01( ):
   '''Wrapper around durtools.naive_prolated_to_written_not_less_than( ) 
   that returns dotted and double dotted durations where appropriate.
   Note that output *does not* increase monotonically.'''

   assert durtools.prolated_to_written_not_less_than(
      Rational(1, 16)) == Rational(1, 16)
   assert durtools.prolated_to_written_not_less_than(
      Rational(2, 16)) == Rational(2, 16)
   assert durtools.prolated_to_written_not_less_than(
      Rational(3, 16)) == Rational(3, 16)
   assert durtools.prolated_to_written_not_less_than(
      Rational(4, 16)) == Rational(4, 16)
   assert durtools.prolated_to_written_not_less_than(
      #Rational(5, 16)) == Rational(8, 16)
      Rational(5, 16)) == Rational(6, 16)
   assert durtools.prolated_to_written_not_less_than(
      Rational(6, 16)) == Rational(6, 16)
   assert durtools.prolated_to_written_not_less_than(
      Rational(7, 16)) == Rational(7, 16)
   assert durtools.prolated_to_written_not_less_than(
      Rational(8, 16)) == Rational(8, 16)
   assert durtools.prolated_to_written_not_less_than(
      #Rational(9, 16)) == Rational(16, 16)
      Rational(9, 16)) == Rational(12, 16)
   assert durtools.prolated_to_written_not_less_than(
      #Rational(10, 16)) == Rational(16, 16)
      Rational(10, 16)) == Rational(12, 16)
   assert durtools.prolated_to_written_not_less_than(
      #Rational(11, 16)) == Rational(16, 16)
      Rational(11, 16)) == Rational(12, 16)
   assert durtools.prolated_to_written_not_less_than(
      Rational(12, 16)) == Rational(12, 16)
