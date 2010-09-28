from abjad import *


def test_durtools_multiply_duration_pair_and_reduce_factors_01( ):
   assert durtools.multiply_duration_pair_and_reduce_factors(
      (4, 8), Fraction(2, 3)) == (4, 12)


def test_durtools_multiply_duration_pair_and_reduce_factors_02( ):
   assert durtools.multiply_duration_pair_and_reduce_factors(
      (4, 8), Fraction(4, 1)) == (4, 2)


def test_durtools_multiply_duration_pair_and_reduce_factors_03( ):
   assert durtools.multiply_duration_pair_and_reduce_factors(
      (4, 8), Fraction(3, 5)) == (12, 40)


def test_durtools_multiply_duration_pair_and_reduce_factors_04( ):
   assert durtools.multiply_duration_pair_and_reduce_factors(
      (4, 8), Fraction(6, 5)) == (12, 20)


def test_durtools_multiply_duration_pair_and_reduce_factors_05( ):
   assert durtools.multiply_duration_pair_and_reduce_factors(
      (5, 6), Fraction(6, 5)) == (1, 1)
