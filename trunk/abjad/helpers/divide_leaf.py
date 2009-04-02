from abjad.helpers.donate import donate
from abjad.helpers.prolated_to_written import _prolated_to_written
from abjad.note.note import Note
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def divide_leaf(leaf, divisions = 2, prolation = 'diminution'):
   '''Newer and better tuplet-maker.
      Compare with divide( ) helper.'''

   # find target duration of fixed-duration tuplet
   target_duration = leaf.duration.written

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / divisions

   # find written duration of each note in tuplet
   written_duration = _prolated_to_written(prolated_duration, prolation)

   # make tuplet notes
   notes = Note(0, written_duration) * divisions

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # give leaf position in score structure to tuplet
   donate([leaf], tuplet)

   # return tuplet
   return tuplet
