from fractions import Fraction


def multiply_duration_pair(pair, multiplier):
   '''.. versionadded:: 1.1.1

   Multiply duration `pair` by rational `multiplier`::

      abjad> durtools.multiply_duration_pair((4, 8), Fraction(4, 5))
      (16, 40)

   Naive multiplication with no simplification of anything intended for certain types of meter multiplication.

   Return integer pair.

   .. versionchanged:: 1.1.2
      renamed ``durtools.pair_multiply_naive( )`` to
      ``durtools.multiply_duration_pair( )``.
   '''

   assert isinstance(pair, tuple)
   assert isinstance(multiplier, Fraction)

   return pair[0] * multiplier.numerator, pair[1] * multiplier.denominator
