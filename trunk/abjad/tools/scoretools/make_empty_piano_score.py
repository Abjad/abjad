from abjad.components.Score import Score
from abjad.components.Staff import Staff
from abjad.tools import marktools
from abjad.tools.scoretools.PianoStaff import PianoStaff
#from abjad.tools.stafftools import Clef


def make_empty_piano_score( ):
   r'''.. versionadded:: 1.1.1
   
   Return new score with piano staff. 
   Piano staff contains treble and bass staves with the appropriate clefs.

   All components are new and empty. ::

      abjad> score, treble, bass = scoretools.make_empty_piano_score( )
      abjad> print score.format
      \new Score <<
         \new PianoStaff <<
            \new Staff {
               \clef "treble"
            }
            \new Staff {
               \clef "bass"
            }
         >>
      >>

   References to the score, treble and bass staves return separately.

   .. versionchanged:: 1.1.2
      renamed ``scoretools.make_piano_staff( )`` to
      ``scoretools.make_empty_piano_score( )``.
   '''

   treble_staff = Staff([ ])
   treble_staff.name = 'treble'
   #treble_staff.clef.forced = Clef('treble')
   marktools.ClefMark('treble')(treble_staff)

   bass_staff = Staff([ ])
   bass_staff.name = 'bass'
   #bass_staff.clef.forced = Clef('bass')
   marktools.ClefMark('bass')(bass_staff)

   piano_staff = PianoStaff([treble_staff, bass_staff])

   score = Score([ ])
   score.append(piano_staff)

   return score, treble_staff, bass_staff
