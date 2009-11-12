from abjad.rational import Rational


def pair_multiply_naive(pair, multiplier):
   '''Multiply `pair` by rational `multiplier`.
   Naive multiplication with no simplification of anything. ::

      abjad> durtools.pair_multiply_naive(4, 8), Rational(4, 5))
      (16, 40)

   ::

      abjad> durtools.pair_multiply_naive(4, 8), Rational(3, 4))
      (12, 32)

   Intended for certain types of meter multiplication.
   '''

   assert isinstance(pair, tuple)
   assert isinstance(multiplier, Rational)

   return pair[0] * multiplier._n, pair[1] * multiplier._d
