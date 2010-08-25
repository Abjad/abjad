from abjad import *


def test_SpanBarInterface_grob_handling_01( ):

   score, treble, bass = scoretools.make_empty_piano_score( )
   treble.extend(macros.scale(4))
   bass.extend(macros.scale(4))
   score.override.span_bar.color = 'red'

   r'''
   \new Score \with {
      \override SpanBar #'color = #red
   } <<
      \new PianoStaff <<
         \context Staff = "treble" {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
         }
         \context Staff = "bass" {
            \clef "bass"
            c'8
            d'8
            e'8
            f'8
         }
      >>
   >>
   '''

   assert componenttools.is_well_formed_component(score)
   assert score.format == '\\new Score \\with {\n\t\\override SpanBar #\'color = #red\n} <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\te\'8\n\t\t\tf\'8\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\tc\'8\n\t\t\td\'8\n\t\t\te\'8\n\t\t\tf\'8\n\t\t}\n\t>>\n>>'
