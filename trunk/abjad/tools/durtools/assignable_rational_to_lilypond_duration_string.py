from abjad.exceptions import AssignabilityError
from abjad.tools.durtools.is_assignable_rational import is_assignable_rational
from abjad.tools.durtools.assignable_rational_to_dot_count import assignable_rational_to_dot_count
from abjad.tools.durtools.rational_to_undotted_lilypond_duration_string import \
   rational_to_undotted_lilypond_duration_string


def assignable_rational_to_lilypond_duration_string(rational):
   '''.. versionadded:: 1.1.2

   Convert `rational` to LilyPond-style duration string. ::

      abjad> durtools.assignable_rational_to_lilypond_duration_string(Rational(3, 16))
      '8.'

   Raise assignability error when `rational` is not notehead-assignable. ::

      abjad> durtools.assignable_rational_to_lilypond_duration_string(Rational(5, 16))
      AssignabilityError

   .. versionchanged:: 1.1.2
      renamed ``durtools.rational_to_duration_string( )`` to
      ``durtools.assignable_rational_to_lilypond_duration_string( )``.
   '''

   if not is_assignable_rational(rational):
      raise AssignabilityError

   undotted_duration_string = rational_to_undotted_lilypond_duration_string(rational)
   dot_count = assignable_rational_to_dot_count(rational)
   dot_string = '.' * dot_count
   duration_string = '%s%s' % (undotted_duration_string, dot_string)

   return duration_string
