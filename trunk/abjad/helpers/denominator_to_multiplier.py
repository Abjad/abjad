from abjad.rational.rational import Rational
from math import log


def _denominator_to_multiplier(d):
   '''
      Given positive integer denominator d,
      get the prolation that d carries.

      Result will always be <= 1.

      abjad> for n in range(1, 19):
      ...     print n, denominator_to_multiplier(n)
      ... 
      1 (1, 1)
      2 (1, 1)
      3 (2, 3)
      4 (1, 1)
      5 (4, 5)
      6 (2, 3)
      7 (4, 7)
      8 (1, 1)
      9 (8, 9)
      10 (4, 5)
      11 (8, 11)
      12 (2, 3)
      13 (8, 13)
      14 (4, 7)
      15 (8, 15)
      16 (1, 1)
      17 (16, 17)
      18 (8, 9)
   '''

   ### TODO - decide whether we need this helper or not;
   ###        may be possible to do with measure.duration.multiplier alone.
      
   assert isinstance(d, int)
   assert d > 0
   while d % 2 == 0:
      d = int(d / 2)
   return Rational(2 ** int(log(d, 2)), d)
