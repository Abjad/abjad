from abjad.rational import Rational


def pair_multiply_constant_numerator(pair, multiplier):
   '''Multiply Python pair by Rational multiplier.
      Hold pair numerator constant, if possible.
      Return new Python pair representing product.

      Intended for certain types of meter multiplication.

      Examples:

      durtools.pair_multiply_constant_numerator(9, 16), Rational(2, 3))
      (9, 24)

      durtools.pair_multiply_constant_numerator(9, 16), Rational(1, 2))
      (9, 32)

      durtools.pair_multiply_constant_numerator(9, 16), Rational(5, 6))
      (45, 96)'''

   assert isinstance(pair, tuple)
   assert isinstance(multiplier, Rational)

   pair_denominator = pair[1]
   candidate_result_denominator = pair_denominator / multiplier
   
   if candidate_result_denominator._d == 1:
      return pair[0], candidate_result_denominator._n
   else:
      result_numerator = pair[0] * candidate_result_denominator._d
      result_denominator = candidate_result_denominator._n
      return result_numerator, result_denominator
