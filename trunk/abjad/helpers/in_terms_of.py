from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.is_divisor_of import _is_divisor_of
from abjad.rational.rational import Rational


def _in_terms_of(q, desired_denominator):
   '''Rewrite q in terms of desired denominator.

   Example:

   >>> for pair in [(n, 6) for n in range(12)]:
   ...     print pair, _in_terms_of(pair, 12)
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
   (11, 6) (22, 12)
   '''

   assert isinstance(q, (Rational, int, long, tuple))
   n, d = _duration_token_unpack(q)
   # if d divides desired denominator
   if _is_divisor_of(d, desired_denominator):
      quotient = desired_denominator / d
      return (n * quotient, d * quotient)
   # if desired denominator divides d
   elif _is_divisor_of(desired_denominator, d):
      quotient = d / desired_denominator
      if _is_divisor_of(quotient, n):
         return (n / quotient, d / quotient)
      else:
         return (n, d)
   # if desired denominator and d are relatively prime
   else:
      return (n, d)
