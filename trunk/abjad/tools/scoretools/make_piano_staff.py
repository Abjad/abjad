from abjad.clef import Clef
from abjad.score import Score
from abjad.staff import Staff
from abjad.staffgroup import PianoStaff


def make_piano_staff( ):
   r'''..versionadded:: 1.1.1
   
   'Return new score with piano staff. 
   Piano staff contains treble and bass staves with the appropriate clefs.

   All components are new and empty. ::

      abjad> score, treble, bass = scoretools.make_piano_staff( )
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
   '''

   treble_staff = Staff([ ])
   treble_staff.clef.forced = Clef('treble')

   bass_staff = Staff([ ])
   bass_staff.clef.forced = Clef('bass')

   piano_staff = PianoStaff([treble_staff, bass_staff])

   score = Score([ ])
   score.append(piano_staff)

   return score, treble_staff, bass_staff
