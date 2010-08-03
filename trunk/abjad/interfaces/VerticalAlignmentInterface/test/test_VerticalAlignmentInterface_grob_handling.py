from abjad import *


def test_VerticalAlignmentInterface_grob_handling_01( ):

   t = Staff(macros.scale(4))
   t.vertical_alignment.staff_padding = 2
   t.vertical_alignment.Y_extent = (-1.5, 1.5)

   r'''
   \new Staff \with {
           \override VerticalAlignment #'Y-extent = #'(-1.5 . 1.5)
           \override VerticalAlignment #'staff-padding = #2
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override VerticalAlignment #'Y-extent = #'(-1.5 . 1.5)\n\t\\override VerticalAlignment #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
