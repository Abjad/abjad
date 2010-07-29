from abjad import *


def test_tempo_interface_tempo_wholes_per_minute_01( ):
   r'''Works with score tempo interface.
   Does not include LilyPond \set command.'''

   t = Staff(macros.scale(4))
   score = Score([t])
   score.tempo.tempo_wholes_per_minute = 24

   r'''
   \new Score \with {
           tempoWholesPerMinute = #(ly:make-moment 24 1)
   } <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert score.format == "\\new Score \\with {\n\ttempoWholesPerMinute = #(ly:make-moment 24 1)\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"


def test_tempo_interface_tempo_wholes_per_minute_02( ):
   r'''Works with leaf tempo interface.
   Includes LilyPond \set command.'''

   t = Staff(macros.scale(4))
   score = Score([t])
   score.leaves[1].tempo.tempo_wholes_per_minute = 24

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   \set Score.tempoWholesPerMinute = #(ly:make-moment 24 1)
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert score.format == "\\new Score <<\n\t\\new Staff {\n\t\tc'8\n\t\t\\set Score.tempoWholesPerMinute = #(ly:make-moment 24 1)\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"
