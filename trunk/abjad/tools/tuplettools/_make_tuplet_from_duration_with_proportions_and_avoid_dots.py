from abjad.exceptions import AssignabilityError
from abjad.components.Note import Note
from abjad.core import Rational
from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools.tuplettools.fix_contents_of_tuplets_in_expr import \
   fix_contents_of_tuplets_in_expr
from abjad.tools.tuplettools.change_augmented_tuplets_in_expr_to_diminished import \
   change_augmented_tuplets_in_expr_to_diminished
from abjad.tools.tuplettools.change_diminished_tuplets_in_expr_to_augmented import \
   change_diminished_tuplets_in_expr_to_augmented
from abjad.components._Tuplet import FixedDurationTuplet


def _make_tuplet_from_duration_with_proportions_and_avoid_dots(
   duration, divisions, prolation):
   '''Divide `duration` according to `divisions`
   and `prolation`.

   Do not allow series of dotted values.
   '''

   ## find basic prolated duration of note in tuplet
   basic_prolated_duration = duration / sum(divisions)

   ## TODO: only this call differs from _duration_into_arbitrary_fixed_duration_tuplet_undotted; so combined the two functions. ##
   ## find basic written duration of note in tuplet
   basic_written_duration = durtools.rational_to_equal_or_greater_binary_rational(
      basic_prolated_duration)
   
   ## find written duration of each note in tuplet
   written_durations = [x * basic_written_duration for x in divisions]

   ## make tuplet notes
   try:
      notes = [Note(0, x) for x in written_durations]
   except AssignabilityError:
      denominator = duration._denominator
      note_durations = [Rational(x, denominator) for x in divisions]
      notes = notetools.make_notes(0, note_durations)

   ## make tuplet
   tuplet = FixedDurationTuplet(duration, notes)

   ## fix tuplet contents if necessary
   fix_contents_of_tuplets_in_expr(tuplet)

   ## switch prolation if necessary
   if not tuplet.duration.multiplier == 1:
      if prolation == 'diminution':
         if not tuplet.duration.diminution:
            change_augmented_tuplets_in_expr_to_diminished(tuplet)
      else:
         if tuplet.duration.diminution:
            change_diminished_tuplets_in_expr_to_augmented(tuplet)

#   ## give leaf position in score structure to tuplet
#   containertools.move_parentage_children_and_spanners_from_components_to_empty_container([l], tuplet)

   ## return tuplet
   return tuplet
