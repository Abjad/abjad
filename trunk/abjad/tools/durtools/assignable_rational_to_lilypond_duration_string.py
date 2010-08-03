from abjad.exceptions import AssignabilityError
from abjad.Rational import Rational
from abjad.tools.durtools.assignable_rational_to_dot_count import assignable_rational_to_dot_count
from abjad.tools.durtools.is_assignable_rational import is_assignable_rational
from abjad.tools.durtools.rational_to_equal_or_lesser_binary_rational \
   import rational_to_equal_or_lesser_binary_rational


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

   undotted_rational = rational_to_equal_or_lesser_binary_rational(rational)
   if undotted_rational <= 1:
      undotted_duration_string = str(undotted_rational._d)
   elif undotted_rational == Rational(2, 1):
      undotted_duration_string = r'\breve'
   elif undotted_rational == Rational(4, 1):
      undotted_duration_string = r'\longa'
   elif undotted_rational == Rational(8, 1):
      undotted_duration_string = r'\maxima'
   else:
      raise ValueError('can not process undotted rational: %s' % undotted_rational)

   dot_count = assignable_rational_to_dot_count(rational)
   dot_string = '.' * dot_count
   dotted_duration_string = undotted_duration_string + dot_string

   return dotted_duration_string
