from abjad import *


def test_measures_tupletize_01( ):
   '''Tupletize one measure, supplement one note.'''

   t = RigidMeasure((4, 8), run(4))
   measures_tupletize(t, run(1))

   r'''
      \time 4/8
      \times 4/5 {
         c'8
         c'8
         c'8
         c'8
         c'8
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 4/8\n\t\\times 4/5 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}"


def test_measures_tupletize_02( ):
   '''Tupletize one measure, supplement one rest.'''

   t = RigidMeasure((4, 8), run(4))
   measures_tupletize(t, [Rest((1, 4))])

   r'''
      \time 4/8
      \times 2/3 {
         c'8
         c'8
         c'8
         c'8
         r4
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 4/8\n\t\\times 2/3 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tr4\n\t}"
