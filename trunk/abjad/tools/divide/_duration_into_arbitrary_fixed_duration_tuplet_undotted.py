from abjad.exceptions import AssignabilityError
from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import construct
from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools import scoretools
from abjad.tuplet import FixedDurationTuplet


def _duration_into_arbitrary_fixed_duration_tuplet_undotted(
   duration, divisions, prolation):
   '''Divide `duration` according to `divisions`
   and `prolation`.

   Do not allow series of dotted values.
   '''

   ## find basic prolated duration of note in tuplet
   basic_prolated_duration = duration / sum(divisions)

   ## TODO: only this call differs from _duration_into_arbitrary_fixed_duration_tuplet_undotted; so combined the two functions. ##
   ## find basic written duration of note in tuplet
   basic_written_duration = durtools.naive_prolated_to_written_not_less_than(
      basic_prolated_duration)
   
   ## find written duration of each note in tuplet
   written_durations = [x * basic_written_duration for x in divisions]

   ## make tuplet notes
   try:
      notes = [Note(0, x) for x in written_durations]
   except AssignabilityError:
      denominator = duration._denominator
      note_durations = [Rational(x, denominator) for x in divisions]
      notes = construct.notes(0, note_durations)

   ## make tuplet
   tuplet = FixedDurationTuplet(duration, notes)

   ## fix tuplet contents if necessary
   tuplettools.contents_fix(tuplet)

   ## switch prolation if necessary
   if not tuplet.duration.multiplier == 1:
      if prolation == 'diminution':
         if not tuplet.duration.diminution:
            tuplettools.augmentation_to_diminution(tuplet)
      else:
         if tuplet.duration.diminution:
            tuplettools.diminution_to_augmentation(tuplet)

#   ## give leaf position in score structure to tuplet
#   scoretools.donate([l], tuplet)

   ## return tuplet
   return tuplet
