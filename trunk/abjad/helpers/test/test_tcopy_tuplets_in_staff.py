from abjad import *


def test_tcopy_tuplets_in_staff_02( ):
   '''Copy adjacent, whole tuplets from staff.'''

   t = Staff(FixedDurationTuplet((2, 8), run(3)) * 3)
   pitches.diatonicize(t)
   u = tcopy(t[1:])

   r'''
   \new Staff {
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
           \times 2/3 {
                   b'8
                   c''8
                   d''8
           }
   }
   '''

   assert check(t)
   assert check(u) 
   assert u.format == "\\new Staff {\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n\t\\times 2/3 {\n\t\tb'8\n\t\tc''8\n\t\td''8\n\t}\n}"
