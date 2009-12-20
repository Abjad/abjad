from abjad import *


def test_DynamicTextSpannerInterface_grob_handling_01( ):

   t = Staff(construct.scale(4))
   t.dynamic_text_spanner.staff_padding = 2
   t.dynamic_text_spanner.Y_extent = (-1.5, 1.5)

   r'''
   \new Staff \with {
           \override DynamicTextSpanner #'Y-extent = #'(-1.5 . 1.5)
           \override DynamicTextSpanner #'staff-padding = #2
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override DynamicTextSpanner #'Y-extent = #'(-1.5 . 1.5)\n\t\\override DynamicTextSpanner #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
