from abjad.rational.rational import Rational
from abjad.tools.durtools.token_unpack import token_unpack

def in_terms_of(q, desired_denominator):
   '''Rewrite *q* in terms of desired denominator.

   Arguments:
      *q* : int, long, Rational, tuple pair
         The pair (a, b) to be expressed in terms of a new denominator 
         b' = *desired_denominator*.
      *desired_denominator* : int
         The new denominator of *q*.

   Returns:
      (a', b') pair. a' = a * *desired_denominator* / b.  
      b' = *desired_denominator*


   Example::

      >>> for pair in [(n, 6) for n in range(12)]:
      ...     print pair, in_terms_of(pair, 12)
      ... 
      (0, 6) (0, 12)
      (1, 6) (2, 12)
      (2, 6) (4, 12)
      (3, 6) (6, 12)
      (4, 6) (8, 12)
      (5, 6) (10, 12)
      (6, 6) (12, 12)
      (7, 6) (14, 12)
      (8, 6) (16, 12)
      (9, 6) (18, 12)
      (10, 6) (20, 12)
      (11, 6) (22, 12)'''

   assert isinstance(q, (Rational, int, long, tuple))
   n, d = token_unpack(q)
   multiplier = Rational(desired_denominator, d)
   new_numerator = multiplier * n
   new_denominator = multiplier * d
   if new_numerator._d == 1 and new_denominator._d == 1:
      return (new_numerator._n, new_denominator._n)
   else:
      return (n, d)
