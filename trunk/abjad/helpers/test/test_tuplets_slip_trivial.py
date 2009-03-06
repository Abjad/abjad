from abjad import *


def test_tuplets_slip_trivial_01( ):
   t = Staff(FixedDurationTuplet((2, 8), run(2)) * 2)
   diatonicize(t)
   assert len(t) == 2

   r'''
   \new Staff {
         c'8
         d'8
         e'8
         f'8
   }
   '''

   tuplets_slip_trivial(t)

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''
   
   assert check(t)
   assert len(t) == 4
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
