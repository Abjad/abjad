from abjad import *


def test_GlissandoSpanner_grob_handling_01( ):
   '''The Abjad Glissando spanner handles the LilyPond Glissando grob.'''

   t = Voice(macros.scale(4))
   p = GlissandoSpanner(t[ : ])
   p.thickness = 3

   r'''
   \new Voice {
      \override Glissando #'thickness = #3
      c'8 \glissando
      d'8 \glissando
      e'8 \glissando
      f'8
      \revert Glissando #'thickness
   }
   '''

   assert t.format == "\\new Voice {\n\t\\override Glissando #'thickness = #3\n\tc'8 \\glissando\n\td'8 \\glissando\n\te'8 \\glissando\n\tf'8\n\t\\revert Glissando #'thickness\n}"
