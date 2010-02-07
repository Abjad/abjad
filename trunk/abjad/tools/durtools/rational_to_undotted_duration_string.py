from abjad.exceptions import AssignabilityError
from abjad.rational import Rational
from abjad.tools.durtools.is_assignable import is_assignable
from abjad.tools.durtools.rational_to_undotted_duration import \
   rational_to_undotted_duration


def rational_to_undotted_duration_string(rational):
   r'''.. versionadded:: 1.1.2

   Convert `rational` to LilyPond-style undotted duration string. ::

      abjad> for n in range(1, 9):
      ...     try:
      ...             rational = Rational(n, 16)
      ...             undotted_duration_string = durtools.rational_to_undotted_duration_string(rational)
      ...             print '%s\t%s' % (rational, undotted_duration_string)
      ...     except AssignabilityError:
      ...             pass
      ... 
      1/16    16
      1/8     8
      3/16    8
      1/4     4
      3/8     4
      7/16    4
      1/2     2

   ::

      abjad> durtools.rational_to_undotted_duration_string(Rational(2, 1))
      '\\breve'
   
   Raise assignability error when `rational` is not note-head-assignable. ::

      abjad> durtools.rational_to_undotted_duration_string(Rational(5, 16))
      AssignabilityError
   '''

   if not is_assignable(rational):
      raise AssignabilityError

   undotted_duration = rational_to_undotted_duration(rational)

   if undotted_duration <= 1:
      return str(undotted_duration._d)
   elif undotted_duration == Rational(2, 1):
      return r'\breve'
   elif undotted_duration == Rational(4, 1):
      return r'\longa'
   elif undotted_duration == Rational(8, 1):
      return r'\maxima'
   else:
      raise ValueError('rational %s can not process.' % rational)
