from abjad.note.note import Note
from abjad.tools import durtools
from abjad.tools import scoretools
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def leaf(l, divisions = 2, prolation = 'diminution'):
   '''Newer and better tuplet-maker.
      Compare with divide.pair( ) tuplet-maker.'''

   # find target duration of fixed-duration tuplet
   target_duration = l.duration.written

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / divisions

   # find written duration of each note in tuplet
   written_duration = durtools.prolated_to_written(prolated_duration, prolation)

   # make tuplet notes
   notes = Note(0, written_duration) * divisions

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # give leaf position in score structure to tuplet
   scoretools.donate([l], tuplet)

   # return tuplet
   return tuplet
