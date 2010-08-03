from abjad import *


def test_StaffInterface_grob_handling_01( ):
   '''Grob handling on Staff.'''

   t = Staff(macros.scale(4))
   t.staff.color = 'red'

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


## TODO: note that this is the expected formatting but that it will not change
## the color of the Staff lines. For this to work the Staff must be stopped 
## and restarted before the change for this to have an effect. 
## Should the GrobHandler be smart enough to see who is contributing the 
## formating and add a \stopStaff\startStaff immediately before the staff 
## contribution IFF the contributor is not a Staff?

def test_StaffInterface_grob_handling_02( ):
   '''grob handling on Leaf.'''

   t = Staff(macros.scale(4))
   t[2].staff.color = 'red'
   overridetools.promote_attribute_to_context_on_grob_handler(t[2].staff, 'color', 'Staff')

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
