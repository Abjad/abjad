from abjad.exceptions import AssignabilityError
from abjad.tools.durtools.is_assignable_duration import is_assignable_duration
from abjad.tools.durtools.rational_to_dot_count import rational_to_dot_count
from abjad.tools.durtools.rational_to_undotted_duration_string import \
   rational_to_undotted_duration_string


def rational_to_duration_string(rational):
   '''.. versionadded:: 1.1.2

   Convert `rational` to LilyPond-style duration string. ::

      abjad> durtools.rational_to_duration_string(Rational(3, 16))
      '8.'

   Raise assignability error when `rational` is not notehead-assignable. ::

      abjad> durtools.rational_to_duration_string(Rational(5, 16))
      AssignabilityError
   '''

   if not is_assignable_duration(rational):
      raise AssignabilityError

   undotted_duration_string = rational_to_undotted_duration_string(rational)
   dot_count = rational_to_dot_count(rational)
   dot_string = '.' * dot_count
   duration_string = '%s%s' % (undotted_duration_string, dot_string)

   return duration_string
