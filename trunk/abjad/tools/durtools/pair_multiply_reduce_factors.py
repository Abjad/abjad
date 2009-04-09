from abjad.rational.rational import Rational
from abjad.tools import mathtools


def pair_multiply_reduce_factors(pair, multiplier):
   '''Multiply Python pair by Rational multiplier.
      Reduce common cross factors.

      Examples:

      durtools.pair_multiply_reduce_factors(4, 8), Rational(2, 3))
      (4, 12)

      durtools.pair_multiply_reduce_factors(4, 8), Rational(6, 5))
      (12, 20)'''

   assert isinstance(pair, tuple)
   assert isinstance(multiplier, Rational)

   pair_numerator_factors = mathtools.factors(pair[0])   
   multiplier_denominator_factors = mathtools.factors(multiplier._d)
   for factor in multiplier_denominator_factors[:]:
      if factor in pair_numerator_factors:
         pair_numerator_factors.remove(factor)
         multiplier_denominator_factors.remove(factor)
   
   pair_denominator_factors = mathtools.factors(pair[1])
   multiplier_numerator_factors = mathtools.factors(multiplier._n)
   for factor in multiplier_numerator_factors[:]:
      if factor in pair_denominator_factors:
         pair_denominator_factors.remove(factor)
         multiplier_numerator_factors.remove(factor)

   result_numerator_factors = pair_numerator_factors + \
      multiplier_numerator_factors
   result_denominator_factors = pair_denominator_factors + \
      multiplier_denominator_factors

   result_numerator = 1
   for factor in result_numerator_factors:
      result_numerator *= factor

   result_denominator = 1
   for factor in result_denominator_factors:
      result_denominator *= factor

   return result_numerator, result_denominator
