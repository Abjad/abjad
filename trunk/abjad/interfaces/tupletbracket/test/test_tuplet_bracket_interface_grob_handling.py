from abjad import *


def test_tuplet_bracket_grob_handling_01( ):
   '''Override LilyPond TupletBracket grob on Abjad voice.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t.tupletbracket.direction = 'down'

   r'''\new Voice \with {
           \override TupletBracket #'direction = #down
   } {
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice \\with {\n\t\\override TupletBracket #'direction = #down\n} {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_tuplet_bracket_grob_handling_02( ):
   '''Override LilyPond TupletBracket grob on Abjad leaf.'''

   t = Voice(construct.scale(4))
   Beam(t[:])
   t[1].tupletbracket.direction = 'down'

   r'''\new Voice {
           c'8 [
           \once \override TupletBracket #'direction = #down
           d'8
           e'8
           f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t\\once \\override TupletBracket #'direction = #down\n\td'8\n\te'8\n\tf'8 ]\n}"
