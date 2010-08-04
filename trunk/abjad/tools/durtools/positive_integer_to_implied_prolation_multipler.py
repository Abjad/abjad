from abjad.core import Rational
from abjad.tools import mathtools


def positive_integer_to_implied_prolation_multipler(denominator):
   '''Return prolation attaching to integer `denominator`.

   ::

      abjad> for denominator in range(1, 17):
      ...     multiplier = durtools.positive_integer_to_implied_prolation_multipler(denominator)
      ...     print '%s\\t%s' % (denominator, multiplier)
      ... 
      1       1
      2       1
      3       2/3
      4       1
      5       4/5
      6       2/3
      7       4/7
      8       1
      9       8/9
      10      4/5
      11      8/11
      12      2/3
      13      8/13
      14      4/7
      15      8/15
      16      1

   .. note:: result always less than or equal to 1.

   .. versionchanged:: 1.1.2
      renamed ``durtools.denominator_to_multiplier( )`` to
      ``durtools.positive_integer_to_implied_prolation_multipler( )``.

   .. versionchanged:: 1.1.2
      renamed ``durtools.integer_denominator_to_implied_prolation( )`` to
      ``durtools.positive_integer_to_implied_prolation_multipler( )``.
   '''

   return Rational(
      mathtools.greatest_power_of_two_less_equal(denominator), denominator)
