from abjad import *


def test_tcopy_notes_in_staff_01( ):
   '''Copy adjacent notes in staff.'''

   t = Staff(scale(4))
   u = tcopy(t[:2])

   r'''
   \new Staff {
           c'8
           d'8
   }
   '''

   assert check.wf(t)
   assert check.wf(u)
   assert u.format == "\\new Staff {\n\tc'8\n\td'8\n}"


def test_tcopy_notes_in_staff_02( ):
   '''Copy adjacent notes in staff.'''

   t = Staff(scale(4))
   u = tcopy(t[-2:])

   r'''
   \new Staff {
           e'8
           f'8
   }
   '''
   
   assert check.wf(t)
   assert check.wf(u)
   assert u.format == "\\new Staff {\n\te'8\n\tf'8\n}"
