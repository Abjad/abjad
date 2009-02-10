from abjad import *


def test_measures_beam_01( ):
   '''Beam all measures in expr.'''

   t = Staff(RigidMeasure((2, 8), run(2)) * 3)
   diatonicize(t)
   measures_beam(t)

   r'''
   \new Staff {
         \time 2/8
         c'8 [
         d'8 ]
         \time 2/8
         e'8 [
         f'8 ]
         \time 2/8
         g'8 [
         a'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'8 [\n\t\td'8 ]\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ]\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ]\n}"
