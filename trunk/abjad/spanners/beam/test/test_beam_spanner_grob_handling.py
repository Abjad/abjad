from abjad import *


def test_beam_spanner_grob_handling_01( ):
   '''
   Abjad Beam spanners handle the LilyPond Beam grob.
   '''

   t = Voice(construct.scale(4))
   p = Beam(t[ : ])
   p.positions = (4, 4)

   r'''
   \new Voice {
      \override Beam #'positions = #'(4 . 4)
      c'8 [
      d'8
      e'8
      f'8 ]
      \revert Beam #'positions
   }
   '''

   assert t.format == "\\new Voice {\n\t\\override Beam #'positions = #'(4 . 4)\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'positions\n}"
