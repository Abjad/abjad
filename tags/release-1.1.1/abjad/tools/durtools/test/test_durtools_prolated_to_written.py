from abjad import *


def test_durtools_prolated_to_written_01( ):
   '''Wrapper around _naivedurtools.prolated_to_written( ) that returns
      dotted and double dotted durations where appropriate.
      Note that output *does not* increase monotonically for diminution.'''

   assert durtools.prolated_to_written(
      Rational(1, 16), 'diminution') == Rational(1, 16)
   assert durtools.prolated_to_written(
      Rational(2, 16), 'diminution') == Rational(2, 16)
   assert durtools.prolated_to_written(
      Rational(3, 16), 'diminution') == Rational(3, 16)
   assert durtools.prolated_to_written(
      Rational(4, 16), 'diminution') == Rational(4, 16)
   assert durtools.prolated_to_written(
      Rational(5, 16), 'diminution') == Rational(8, 16)
   assert durtools.prolated_to_written(
      Rational(6, 16), 'diminution') == Rational(6, 16)
   assert durtools.prolated_to_written(
      Rational(7, 16), 'diminution') == Rational(7, 16)
   assert durtools.prolated_to_written(
      Rational(8, 16), 'diminution') == Rational(8, 16)
   assert durtools.prolated_to_written(
      Rational(9, 16), 'diminution') == Rational(16, 16)
   assert durtools.prolated_to_written(
      Rational(10, 16), 'diminution') == Rational(16, 16)
   assert durtools.prolated_to_written(
      Rational(11, 16), 'diminution') == Rational(16, 16)
   assert durtools.prolated_to_written(
      Rational(12, 16), 'diminution') == Rational(12, 16)


def test_durtools_prolated_to_written_02( ):
   '''Wrapper around _naivedurtools.prolated_to_written( ) that returns
      dotted and double dotted durations where appropriate.
      Note that output *does* increase monotonically for augmentation.'''

   assert durtools.prolated_to_written(
      Rational(1, 16), 'augmentation') == Rational(1, 16)
   assert durtools.prolated_to_written(
      Rational(2, 16), 'augmentation') == Rational(2, 16)
   assert durtools.prolated_to_written(
      Rational(3, 16), 'augmentation') == Rational(3, 16)
   assert durtools.prolated_to_written(
      Rational(4, 16), 'augmentation') == Rational(4, 16)
   assert durtools.prolated_to_written(
      Rational(5, 16), 'augmentation') == Rational(4, 16)
   assert durtools.prolated_to_written(
      Rational(6, 16), 'augmentation') == Rational(6, 16)
   assert durtools.prolated_to_written(
      Rational(7, 16), 'augmentation') == Rational(7, 16)
   assert durtools.prolated_to_written(
      Rational(8, 16), 'augmentation') == Rational(8, 16)
   assert durtools.prolated_to_written(
      Rational(9, 16), 'augmentation') == Rational(8, 16)
   assert durtools.prolated_to_written(
      Rational(10, 16), 'augmentation') == Rational(8, 16)
   assert durtools.prolated_to_written(
      Rational(11, 16), 'augmentation') == Rational(8, 16)
   assert durtools.prolated_to_written(
      Rational(12, 16), 'augmentation') == Rational(12, 16)
