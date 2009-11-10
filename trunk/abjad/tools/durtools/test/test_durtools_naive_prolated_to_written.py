#from abjad import *
#
#
#def test_durtools_naive_prolated_to_written_01( ):
#   '''Return least written duration of the form 1 / 2 ** n, such that
#      written duration is greater than or equal to prolated duration.'''
#
#   assert durtools.naive_prolated_to_written(
#      Rational(1, 80), 'diminution') == Rational(1, 64)
#   assert durtools.naive_prolated_to_written(
#      Rational(2, 80), 'diminution') == Rational(1, 32)
#   assert durtools.naive_prolated_to_written(
#      Rational(3, 80), 'diminution') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(4, 80), 'diminution') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(5, 80), 'diminution') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(6, 80), 'diminution') == Rational(1, 8)
#   assert durtools.naive_prolated_to_written(
#      Rational(7, 80), 'diminution') == Rational(1, 8)
#   assert durtools.naive_prolated_to_written(
#      Rational(8, 80), 'diminution') == Rational(1, 8)
#   assert durtools.naive_prolated_to_written(
#      Rational(9, 80), 'diminution') == Rational(1, 8)
#   assert durtools.naive_prolated_to_written(
#      Rational(10, 80), 'diminution') == Rational(1, 8)
#   assert durtools.naive_prolated_to_written(
#      Rational(11, 80), 'diminution') == Rational(1, 4)
#   assert durtools.naive_prolated_to_written(
#      Rational(12, 80), 'diminution') == Rational(1, 4)
#
#
#def test_durtools_naive_prolated_to_written_02( ):
#   '''Return greatest written duration of the form 1 / 2 ** n, such that
#      written duration is less than or equal to prolated duration.'''
#
#   assert durtools.naive_prolated_to_written(
#      Rational(1, 80), 'augmentation') == Rational(1, 128)
#   assert durtools.naive_prolated_to_written(
#      Rational(2, 80), 'augmentation') == Rational(1, 64)
#   assert durtools.naive_prolated_to_written(
#      Rational(3, 80), 'augmentation') == Rational(1, 32)
#   assert durtools.naive_prolated_to_written(
#      Rational(4, 80), 'augmentation') == Rational(1, 32)
#   assert durtools.naive_prolated_to_written(
#      Rational(5, 80), 'augmentation') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(6, 80), 'augmentation') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(7, 80), 'augmentation') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(8, 80), 'augmentation') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(9, 80), 'augmentation') == Rational(1, 16)
#   assert durtools.naive_prolated_to_written(
#      Rational(10, 80), 'augmentation') == Rational(1, 8)
#   assert durtools.naive_prolated_to_written(
#      Rational(11, 80), 'augmentation') == Rational(1, 8)
#   assert durtools.naive_prolated_to_written(
#      Rational(12, 80), 'augmentation') == Rational(1, 8)
