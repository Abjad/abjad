from abjad import *


def test_StaffInterface_line_positions_01( ):

   staff = Staff(macros.scale(4))
   staff.staff.line_positions = schemetools.SchemeVector(-4, -2, 2, 4)

   r'''
   \new Staff \with {
           \override StaffSymbol #'line-positions = #'(-4 -2 2 4)
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert staff.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'line-positions = #'(-4 -2 2 4)\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
