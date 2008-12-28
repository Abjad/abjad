from abjad import *


def test_grob_override_01( ):
   '''
   Tuplets bracket grob overrides at opening and closing.
   '''

   t = FixedDurationTuplet((2, 8), scale(3))
   t.glissando.thickness = 3

   r'''
   \times 2/3 {
      \override Glissando #'thickness = #3
      c'8
      d'8
      e'8
      \revert Glissando #'thickness
   }
   '''

   assert t.format == "\\times 2/3 {\n\t\\override Glissando #'thickness = #3\n\tc'8\n\td'8\n\te'8\n\t\\revert Glissando #'thickness\n}"
