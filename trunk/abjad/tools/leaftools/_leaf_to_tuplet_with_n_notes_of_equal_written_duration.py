from abjad.note import Note
from abjad.tools import durtools
from abjad.tools import scoretools
from abjad.tuplet import FixedDurationTuplet


def _leaf_to_tuplet_with_n_notes_of_equal_written_duration(l, divisions, prolation):
   '''Divide written duration of `l` according to `divisions`
   and `prolation`.
   '''

   # find target duration of fixed-duration tuplet
   target_duration = l.duration.written

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / divisions

   # find written duration of each note in tuplet
   if prolation == 'diminution':
      written_duration = durtools.prolated_to_written_not_less_than(
         prolated_duration)
   elif prolation == 'augmentation':
      written_duration = durtools.prolated_to_written_not_greater_than(
         prolated_duration)
   else:
      raise ValueError('must be diminution or augmentation.')

   # make tuplet notes
   notes = Note(0, written_duration) * divisions

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # give leaf position in score structure to tuplet
   scoretools.donate([l], tuplet)

   # return tuplet
   return tuplet
