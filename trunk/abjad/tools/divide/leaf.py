from abjad.note import Note
from abjad.tools import durtools
from abjad.tools import scoretools
from abjad.tuplet import FixedDurationTuplet


def leaf(l, divisions = 2, prolation = 'diminution'):
   '''Divide the written duration of `l` according to `divisions`.

   ::

      abjad> for divisions in range(1, 6):
      ...     note = Note(0, (3, 16))
      ...     tuplet = divide.leaf(note, divisions = divisions, prolation = 'diminution')
      ...     print tuplet
      ... 
      {@ 1:1 c'8. @}
      {@ 1:1 c'16., c'16. @}
      {@ 1:1 c'16, c'16, c'16 @}
      {@ 1:1 c'32., c'32., c'32., c'32. @}
      {@ 5:3 c'16, c'16, c'16, c'16, c'16 @}

   Compare with :func:`divide.pair()
   <abjad.tools.divide.pair>`.
   '''

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
