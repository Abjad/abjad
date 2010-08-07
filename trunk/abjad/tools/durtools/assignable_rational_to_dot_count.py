from abjad.exceptions import AssignabilityError
from abjad.tools import mathtools
from abjad.tools.durtools.is_assignable_rational import is_assignable_rational


def assignable_rational_to_dot_count(rational):
   r'''.. versionadded:: 1.1.2

   Convert `rational` to nonnegative integer number of dots 
   required to represent as LilyPond-style duration string. ::

      abjad> for n in range(1, 9):
      ...     try:
      ...             rational = Rational(n, 16)
      ...             dot_count = durtools.assignable_rational_to_dot_count(rational)
      ...             print '%s\t%s' % (rational, dot_count)
      ...     except AssignabilityError:
      ...             pass
      ... 

      1/16    0
      1/8     0
      3/16    1
      1/4     0
      3/8     1
      7/16    2
      1/2     0

   Raise assignability error when `rational` is not note-head-assignable. ::

      abjad> durtools.assignable_rational_to_dot_count(Rational(5, 16))
      AssignabilityError

   .. versionchanged:: 1.1.2
      renamed ``durtools.rational_to_dot_count( )`` to
      ``durtools.assignable_rational_to_dot_count( )``.
   '''

   if not is_assignable_rational(rational):
      raise AssignabilityError

   binary_string = mathtools.integer_to_binary_string(rational._n)
   digit_sum = sum([int(x) for x in list(binary_string)])
   dot_count = digit_sum - 1
   
   return dot_count
