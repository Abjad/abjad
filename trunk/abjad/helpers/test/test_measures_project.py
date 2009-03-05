from abjad import *


def test_measures_project_01( ):
   '''Project 3/12 meter onto measure contents.'''

   inner = FixedDurationTuplet((2, 16), run(3, Rational(1, 16)))
   notes = run(2)
   outer = FixedDurationTuplet((2, 8), [inner] + notes)
   t = RigidMeasure((2, 8), [outer])
   diatonicize(t)
   measures_subsume(t)

   r'''
      \time 3/12
      \scaleDurations #'(2 . 3) {
         \times 2/3 {
            c'16
            d'16
            e'16
         }
         f'8
         g'8
      }
   '''

   measures_project(t)

   r'''
      \time 2/8
      \times 2/3 {
         \times 2/3 {
            c'16
            d'16
            e'16
         }
         f'8
         g'8
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 2/8\n\t\\times 2/3 {\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t}\n\t\tf'8\n\t\tg'8\n\t}"
