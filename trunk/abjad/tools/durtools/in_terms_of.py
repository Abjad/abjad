from abjad.rational import Rational
from abjad.tools.durtools.token_unpack import token_unpack


def in_terms_of(duration, desired_denominator):
   r'''Rewrite `duration` as a pair
   with positive integer `desired_denominator`. ::

      abjad> for n in range(1, 17):
      ...     rational = Rational(n, 16)
      ...     pair = durtools.in_terms_of(rational, 16)
      ...     print '%s\t%s' % (rational, pair)
      ... 
      1/16    (1, 16)
      1/8     (2, 16)
      3/16    (3, 16)
      1/4     (4, 16)
      5/16    (5, 16)
      3/8     (6, 16)
      7/16    (7, 16)
      1/2     (8, 16)
      9/16    (9, 16)
      5/8     (10, 16)
      11/16   (11, 16)
      3/4     (12, 16)
      13/16   (13, 16)
      7/8     (14, 16)
      15/16   (15, 16)
      1       (16, 16)
   '''

   assert isinstance(duration, (Rational, int, long, tuple))
   n, d = token_unpack(duration)
   multiplier = Rational(desired_denominator, d)
   new_numerator = multiplier * n
   new_denominator = multiplier * d
   if new_numerator._d == 1 and new_denominator._d == 1:
      return (new_numerator._n, new_denominator._n)
   else:
      return (n, d)
