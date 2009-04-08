from abjad.tools import mathtools
from abjad.rational.rational import Rational


def _denominator_to_multiplier(d):
   '''
   Return prolation attaching to denominator 'd'; result always <= 1.

   abjad> for n in range(1, 9):
   ...     print n, _denominator_to_multiplier(n)
   ... 
   1 1
   2 1
   3 2/3
   4 1
   5 4/5
   6 2/3
   7 4/7
   8 1

   See helpers/test/test_denominator_to_multiplier.py for examples.
   '''

   return Rational(mathtools.next_least_power_of_two(d), d)
