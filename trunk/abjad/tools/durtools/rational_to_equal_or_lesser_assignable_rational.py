from abjad.Rational import Rational
from abjad.tools import mathtools
from abjad.tools.durtools.is_assignable_rational import is_assignable_rational
from abjad.tools.durtools.rational_to_equal_or_lesser_binary_rational \
   import rational_to_equal_or_lesser_binary_rational \
   as durtools_rational_to_equal_or_lesser_binary_rational
import math


def rational_to_equal_or_lesser_assignable_rational(prolated_duration):
   '''Return the greatest note-head-assignable rational not greater than
   `prolated_duration`. ::

      abjad> for n in range(1, 17):
      ...     prolated = Rational(n, 16)
      ...     written = durtools.rational_to_equal_or_lesser_assignable_rational(prolated)
      ...     print '%s/16\\t%s' % (n, written)
      ... 
      1/16    1/16
      2/16    1/8
      3/16    3/16
      4/16    1/4
      5/16    1/4
      6/16    3/8
      7/16    7/16
      8/16    1/2
      9/16    1/2
      10/16   1/2
      11/16   1/2
      12/16   3/4
      13/16   3/4
      14/16   7/8
      15/16   15/16
      16/16   1

   .. note:: this function returns dotted and double dotted durations
      where possible.

   .. versionchanged:: 1.1.2
      Fixed to produce monotonically increasing output
      in response to monotonically increasing input.

   .. versionchanged:: 1.1.2
      renamed ``durtools.prolated_to_written_not_greater_than( )`` to
      ``durtools.rational_to_equal_or_lesser_assignable_rational( )``.
   '''

#   if is_assignable_rational(prolated_duration):
#      return prolated_duration
#   else:
#      return durtools_rational_to_equal_or_lesser_binary_rational(
#         prolated_duration)

   good_denominator = mathtools.least_power_of_two_greater_equal(
      prolated_duration._d)

   cur_numerator = prolated_duration._n
   candidate = Rational(cur_numerator, good_denominator)

   while not is_assignable_rational(candidate):
      cur_numerator -= 1
      candidate = Rational(cur_numerator, good_denominator)
      
   return candidate
