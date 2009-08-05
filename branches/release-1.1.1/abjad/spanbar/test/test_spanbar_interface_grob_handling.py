from abjad import *


def test_spanbar_interface_grob_handling_01( ):

   score, treble, bass = scoretools.make_piano_staff( )
   score.spanbar.color = 'red'

   r'''\new Score \with {
           \override SpanBar #'color = #red
   } <<
           \new PianoStaff <<
                   \context Staff = "treble" {
                           \clef "treble"
                   }
                   \context Staff = "bass" {
                           \clef "bass"
                   }
           >>
   >>'''

   assert check.wf(score)
   assert score.format == '\\new Score \\with {\n\t\\override SpanBar #\'color = #red\n} <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t}\n\t>>\n>>'
