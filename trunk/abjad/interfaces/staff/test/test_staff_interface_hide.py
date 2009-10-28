from abjad import *


def test_staff_interface_hide_01( ):
   '''Hide staff around one measure.'''

   t = Staff(RigidMeasure((2, 8), construct.scale(2)) * 3)
   pitchtools.diatonicize(t)

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
           }
           {
                   \time 2/8
                   g'8
                   a'8
           }
   }
   '''

   t[1].staff.hide = True

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   \stopStaff
                   e'8
                   f'8
                   \startStaff
           }
           {
                   \time 2/8
                   g'8
                   a'8
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\t\\stopStaff\n\t\te'8\n\t\tf'8\n\t\t\\startStaff\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_staff_interface_hide_02( ):
   '''Hide staff around one leaf.'''

   t = Note(0, (1, 8))
   t.staff.hide = True

   r'''
   \stopStaff
   c'8
   \startStaff
   '''

   assert check.wf(t)
   assert t.format == "\\stopStaff\nc'8\n\\startStaff"
