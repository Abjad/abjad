from abjad import *
from abjad.tools import construct


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

   assert t.format == "\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t}\n\t\tf'8\n\t\tg'8\n\t}"

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


def test_measures_project_02( ):
   '''Project nonbinary meter onto measure with tied note values.'''

   t = RigidMeasure((5, 8), [FixedDurationTuplet((5, 8), scale(6))])
   measures_subsume(t)

   r'''
      \time 15/24
      \scaleDurations #'(2 . 3) {
         c'8 ~
         c'32
         d'8 ~
         d'32
         e'8 ~
         e'32
         f'8 ~
         f'32
         g'8 ~
         g'32
         a'8 ~
         a'32
      }
   '''

   assert t.format == "\t\\time 15/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8 ~\n\t\tc'32\n\t\td'8 ~\n\t\td'32\n\t\te'8 ~\n\t\te'32\n\t\tf'8 ~\n\t\tf'32\n\t\tg'8 ~\n\t\tg'32\n\t\ta'8 ~\n\t\ta'32\n\t}"

   measures_project(t)

   r'''
      \time 5/8
      \fraction \times 5/6 {
         c'8
         d'8
         e'8
         f'8
         g'8
         a'8
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 5/8\n\t\\fraction \\times 5/6 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}"
