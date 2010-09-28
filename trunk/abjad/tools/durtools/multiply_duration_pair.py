from abjad.core import Fraction


def multiply_duration_pair(pair, multiplier):
   '''Multiply `pair` by rational `multiplier`.
   Naive multiplication with no simplification of anything. ::

      abjad> durtools.multiply_duration_pair((4, 8), Fraction(4, 5))
      (16, 40)

   ::

      abjad> durtools.multiply_duration_pair(*4, 8), Fraction(3, 4))
      (12, 32)

   Intended for certain types of meter multiplication.

   .. versionchanged:: 1.1.2
      renamed ``durtools.pair_multiply_naive( )`` to
      ``durtools.multiply_duration_pair( )``.
   '''

   assert isinstance(pair, tuple)
   assert isinstance(multiplier, Fraction)

   return pair[0] * multiplier.numerator, pair[1] * multiplier.denominator
