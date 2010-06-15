from abjad import *


def test_scoretools_make_piano_staff_01( ):

   score, treble, bass = scoretools.make_piano_staff( )

   r'''
   \new Score <<
      \new PianoStaff <<
         \context Staff = "treble" {
            \clef "treble"
         }
         \context Staff = "bass" {
            \clef "bass"
         }
      >>
   >>
   '''

   assert componenttools.is_well_formed_component(score)
   assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t}\n\t>>\n>>'
