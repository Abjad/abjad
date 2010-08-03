from abjad.Rational import Rational
import math


def rational_to_equal_or_lesser_binary_rational(prolated_duration):
   '''Return the greatest rational of the form ``1/2**n`` 
   less than or equal to `prolated_duration`. ::

      abjad> for n in range(1, 17):
      ...     prolated_duration = Rational(n, 16)
      ...     written_duration = durtools.rational_to_equal_or_lesser_binary_rational(prolated_duration)
      ...     print '%s/16\\t%s' % (n, written_duration)
      ... 
      1/16    1/16
      2/16    1/8
      3/16    1/8
      4/16    1/4
      5/16    1/4
      6/16    1/4
      7/16    1/4
      8/16    1/2
      9/16    1/2
      10/16   1/2
      11/16   1/2
      12/16   1/2
      13/16   1/2
      14/16   1/2
      15/16   1/2
      16/16   1

   ::

      abjad> durtools.rational_to_equal_or_lesser_binary_rational(Rational(1, 80))
      Rational(1, 128)

   Function intended to find written duration of notes inside tuplet.

   .. versionchanged:: 1.1.2
      renamed ``durtools.naive_prolated_to_written_not_greater_than( )`` to
      ``durtools.rational_to_equal_or_lesser_binary_rational( )``.
   '''

   ## find exponent of denominator
   exponent = -int(math.floor(math.log(prolated_duration, 2)))

   ## find written duration 
   written_duration = Rational(1, 2) ** exponent

   ## return written duration
   return written_duration
