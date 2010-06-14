from abjad import *


def test_DynamicLineSpannerInterface_grob_handling_01( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.dynamic_line_spanner.staff_padding = 2
   t.dynamic_line_spanner.Y_extent = (-1.5, 1.5)

   r'''
   \new Staff \with {
           \override DynamicLineSpanner #'Y-extent = #'(-1.5 . 1.5)
           \override DynamicLineSpanner #'staff-padding = #2
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override DynamicLineSpanner #'Y-extent = #'(-1.5 . 1.5)\n\t\\override DynamicLineSpanner #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
