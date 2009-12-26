from abjad import *


def test_leaftools_shorten_01( ):

   t = Staff(construct.scale(4))
   Slur(t[:])

   leaftools.shorten(t.leaves[1], (1, 32))

   r'''
   \new Staff {
      c'8 (
      d'32
      r16.
      e'8
      f'8 )
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 (\n\td'32\n\tr16.\n\te'8\n\tf'8 )\n}"
