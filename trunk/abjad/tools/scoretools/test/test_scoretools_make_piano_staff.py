from abjad import *


def test_scoretools_make_piano_staff_01( ):

   score, treble, bass = scoretools.make_piano_staff( )

   r'''\new Score <<
      \new PianoStaff <<
         \new Staff {
            \clef "treble"
         }
         \new Staff {
            \clef "bass"
         }
      >>
   >>'''

   assert check.wf(score)
   assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\new Staff {\n\t\t\t\\clef "treble"\n\t\t}\n\t\t\\new Staff {\n\t\t\t\\clef "bass"\n\t\t}\n\t>>\n>>'
