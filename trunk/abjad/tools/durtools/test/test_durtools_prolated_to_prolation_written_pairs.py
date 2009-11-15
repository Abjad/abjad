from abjad import *


def test_durtools_prolated_to_prolation_written_pairs_01( ):

   pairs = durtools.prolated_to_prolation_written_pairs(Rational(1, 8))

   assert pairs == (
      (Rational(1, 1), Rational(1, 8)),
      (Rational(2, 3), Rational(3, 16)),
      (Rational(4, 3), Rational(3, 32)),
      (Rational(4, 7), Rational(7, 32)),
      (Rational(8, 7), Rational(7, 64)),
      (Rational(8, 15), Rational(15, 64)),
      (Rational(16, 15), Rational(15, 128)),
      (Rational(16, 31), Rational(31, 128)))


def test_durtools_prolated_to_prolation_written_pairs_02( ):


   pairs = durtools.prolated_to_prolation_written_pairs(Rational(1, 12))

   assert pairs == (
      (Rational(2, 3), Rational(1, 8)),
      (Rational(4, 3), Rational(1, 16)),
      (Rational(8, 9), Rational(3, 32)),
      (Rational(16, 9), Rational(3, 64)),
      (Rational(16, 21), Rational(7, 64)),
      (Rational(32, 21), Rational(7, 128)),
      (Rational(32, 45), Rational(15, 128)))


def test_durtools_prolated_to_prolation_written_pairs_03( ):


   pairs = durtools.prolated_to_prolation_written_pairs(Rational(5, 48))

   assert pairs == (
      (Rational(5, 6), Rational(1, 8)),
      (Rational(5, 3), Rational(1, 16)),
      (Rational(5, 9), Rational(3, 16)),
      (Rational(10, 9), Rational(3, 32)),
      (Rational(20, 21), Rational(7, 64)),
      (Rational(40, 21), Rational(7, 128)),
      (Rational(8, 9), Rational(15, 128)))
