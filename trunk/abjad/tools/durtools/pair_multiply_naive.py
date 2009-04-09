from abjad.rational.rational import Rational


def pair_multiply_naive(pair, multiplier):
   '''Multiply Python pair by Rational multiplier.
      Naive multiplication with no simplification of anything.

      Intended for certain types of meter multiplication.

      Examples:

      durtools.pair_multiply_naive(4, 8), Rational(4, 5))
      (16, 40)

      durtools.pair_multiply_naive(4, 8), Rational(3, 4))
      (12, 32)'''

   assert isinstance(pair, tuple)
   assert isinstance(multiplier, Rational)

   return pair[0] * multiplier._n, pair[1] * multiplier._d
