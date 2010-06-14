from abjad import *


def test_staff_interface_font_size_01( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.staff.font_size = -3

   r'''
   \new Staff \with {
           fontSize = #-3
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff \\with {\n\tfontSize = #-3\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
