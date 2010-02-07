from abjad.exceptions import AssignabilityError
from abjad.rational import Rational
import math


def rational_to_undotted_duration(rational):
   r'''.. versionadded:: 1.1.2

   Convert `rational` to undotted duration. ::

      abjad> for n in range(1, 9):
      ...     rational = Rational(n, 16)
      ...     undotted_duration = durtools.rational_to_undotted_duration(rational)
      ...     print '%s\t%s' % (rational, undotted_duration)
      ... 
      1/16    1/16
      1/8     1/8
      3/16    1/8
      1/4     1/4
      5/16    1/4
      3/8     1/4
      7/16    1/4
      1/2     1/2
   '''

   exponent = int(math.ceil(math.log(~rational, 2)))
   undotted_duration = Rational(1, 2) ** exponent

   return undotted_duration
