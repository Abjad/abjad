from abjad import *


def test_StaffInterface_grob_handling_01( ):

   t = Staff(macros.scale(4))
   t.override.staff_symbol.color = 'red'

   r'''
   \new Staff \with {
           \override StaffSymbol #'color = #red
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''
 
   assert t.format == "\\new Staff \\with {\n\t\\override StaffSymbol #'color = #red\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_StaffInterface_grob_handling_02( ):

   t = Staff(macros.scale(4))
   t[2].override.staff.staff_symbol.color = 'red'

   r'''
   \new Staff {
           c'8
           d'8
           \once \override Staff.StaffSymbol #'color = #red
           e'8
           f'8
   }
   '''

   t.format == "\\new Staff {\n\tc'8\n\td'8\n\t\\once \\override Staff.StaffSymbol #'color = #red\n\te'8\n\tf'8\n}"
