from abjad import *


def test_HairpinSpanner_grob_handling_01( ):
   '''
   The Abjad Hairpin handles the LilyPond DynamicLineSpanner grob.
   '''

   t = Voice(macros.scale(4))
   p = HairpinSpanner(t[ : ], 'p < f')
   p.staff_padding = 4

   r'''
   \new Voice {
      \override DynamicLineSpanner #'staff-padding = #4
      c'8 \< \p
      d'8
      e'8
      f'8 \f
      \revert DynamicLineSpanner #'staff-padding
   }
   '''

   #assert t.format == "\\new Voice {\n\t\\override DynamicLineSpanner #'staff-padding = #4\n\tc'8 \\< \\pX\n\td'8\n\te'8\n\tf'8 \\fX\n\t\\revert DynamicLineSpanner #'staff-padding\n}"
   assert t.format == "\\new Voice {\n\t\\override DynamicLineSpanner #'staff-padding = #4\n\tc'8 \\< \\p\n\td'8\n\te'8\n\tf'8 \\f\n\t\\revert DynamicLineSpanner #'staff-padding\n}"
