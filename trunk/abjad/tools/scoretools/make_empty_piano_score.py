from abjad.Clef import Clef
from abjad.Score import Score
from abjad.Staff import Staff
from abjad.StaffGroup import PianoStaff


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
   treble_staff.clef.forced = Clef('treble')

   bass_staff = Staff([ ])
   bass_staff.name = 'bass'
   bass_staff.clef.forced = Clef('bass')

   piano_staff = PianoStaff([treble_staff, bass_staff])

   score = Score([ ])
   score.append(piano_staff)

   return score, treble_staff, bass_staff
