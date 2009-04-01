from abjad import *


def test_tuplet_number_grob_handling_01( ):
   '''Override LilyPond TupletNumber grob on Abjad voice.'''

   t = Voice(scale(4))
   Beam(t[:])
   t.tupletnumber.fraction = True

   r'''\new Voice \with {
           \override TupletNumber #'fraction = ##t
   } {
           c'8 [
           d'8
           e'8
           f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice \\with {\n\t\\override TupletNumber #'fraction = ##t\n} {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_tuplet_number_grob_handling_02( ):
   '''Override LilyPond TupletNumber grob on Abjad leaf.'''

   t = Voice(scale(4))
   Beam(t[:])
   t[1].tupletnumber.fraction = True

   r'''\new Voice {
           c'8 [
           \once \override TupletNumber #'fraction = ##t
           d'8
           e'8
           f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t\\once \\override TupletNumber #'fraction = ##t\n\td'8\n\te'8\n\tf'8 ]\n}"
