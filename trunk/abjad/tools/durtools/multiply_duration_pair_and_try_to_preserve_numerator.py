from abjad.core import Fraction


def multiply_duration_pair_and_try_to_preserve_numerator(pair, multiplier):
   '''Multiply `pair` by rational `multiplier`.
   Hold `pair` numerator constant, if possible.
   Return new pair. ::

      abjad> durtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(2, 3))
      (9, 24)

   ::

      abjad> durtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(1, 2))
      (9, 32)

   ::

      abjad> durtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(5, 6))
      (45, 96)

   Intended for certain types of meter multiplication.

   .. versionchanged:: 1.1.2
      renamed ``durtools.pair_multiply_constant_numerator( )`` to
      ``durtools.multiply_duration_pair_and_try_to_preserve_numerator( )``.
   '''

   assert isinstance(pair, tuple)
   assert isinstance(multiplier, Fraction)

   pair_denominator = pair[1]
   candidate_result_denominator = pair_denominator / multiplier
   
   if candidate_result_denominator.denominator == 1:
      return pair[0], candidate_result_denominator.numerator
   else:
      result_numerator = pair[0] * candidate_result_denominator.denominator
      result_denominator = candidate_result_denominator.numerator
      return result_numerator, result_denominator
