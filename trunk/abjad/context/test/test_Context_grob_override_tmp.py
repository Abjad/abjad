from abjad import *


def test_Context_grob_override_tmp_01( ):
   '''Contexts override grobs in their with block.
   '''

   t = Voice(macros.scale(4))
   t.glissando.thickness = 3

   r'''
   \new Voice \with {
      \override Glissando #'thickness = #3
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t.format == "\\new Voice \\with {\n\t\\override Glissando #'thickness = #3\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
