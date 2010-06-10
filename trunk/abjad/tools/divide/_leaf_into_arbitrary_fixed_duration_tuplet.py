from abjad.exceptions import AssignabilityError
from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import construct
from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools import scoretools
from abjad.tuplet import FixedDurationTuplet


def _leaf_into_arbitrary_fixed_duration_tuplet(l, divisions, prolation):
   '''Divide written duration of `l` according to `divisions`
   and `prolation`.
   '''

   ## find target duration of fixed-duration tuplet
   target_duration = l.duration.written

   ## find basic prolated duration of note in tuplet
   basic_prolated_duration = target_duration / sum(divisions)

   ## find basic written duration of note in tuplet
   basic_written_duration = durtools.prolated_to_written_not_less_than(
      basic_prolated_duration)
   
   ## find written duration of each note in tuplet
   written_durations = [x * basic_written_duration for x in divisions]

   ## make tuplet notes
   try:
      notes = [Note(0, x) for x in written_durations]
   except AssignabilityError:
      denominator = target_duration._denominator
      note_durations = [Rational(x, denominator) for x in divisions]
      notes = construct.notes(0, note_durations)

   ## make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   ## fix tuplet contents if necessary
   tuplettools.fix_contents_of_tuplets_in_expr(tuplet)

   ## switch prolation if necessary
   if not tuplet.duration.multiplier == 1:
      if prolation == 'diminution':
         if not tuplet.duration.diminution:
            tuplettools.change_augmented_tuplets_in_expr_to_diminished(tuplet)
      else:
         if tuplet.duration.diminution:
            tuplettools.change_diminished_tuplets_in_expr_to_augmented(tuplet)

   ## give leaf position in score structure to tuplet
   scoretools.donate([l], tuplet)

   ## return tuplet
   return tuplet
