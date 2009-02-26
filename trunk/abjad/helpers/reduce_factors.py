from abjad.helpers.factors import _factors


def _reduce_factors(pair, multiplier):
   '''Multiply pair by multiplier after having first
      reduced factors in multiplier from pair.

      Examples:

      _reduce_factors((4, 8), Rational(2, 3))
      (4, 12)

      _reduce_factors((4, 8), Rational(6, 5))
      (12, 20)'''

   pair_numerator_factors = _factors(pair[0])   
   multiplier_denominator_factors = _factors(multiplier._d)
   for factor in multiplier_denominator_factors[:]:
      if factor in pair_numerator_factors:
         pair_numerator_factors.remove(factor)
         multiplier_denominator_factors.remove(factor)
   
   pair_denominator_factors = _factors(pair[1])
   multiplier_numerator_factors = _factors(multiplier._n)
   for factor in multiplier_numerator_factors[:]:
      if factor in pair_denominator_factors:
         pair_denominator_factors.remove(factor)
         multiplier_numerator_factors.remove(factor)

   result_numerator_factors = pair_numerator_factors + \
      multiplier_numerator_factors
   result_denominator_factors = pair_denominator_factors + \
      multiplier_denominator_factors

   result_numerator = result_numerator_factors[0]
   for factor in result_numerator_factors[1:]:
      result_numerator *= factor

   result_denominator = result_denominator_factors[0]
   for factor in result_denominator_factors[1:]:
      result_denominator *= factor

   return result_numerator, result_denominator
