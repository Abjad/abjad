from abjad import *


def test_measures_subsume_01( ):
   '''Subsume complete binary tuplet.'''

   t = RigidMeasure((2, 8), [FixedDurationTuplet((2, 8), scale(3))])
   measures_subsume(t)

   r'''
      \time 3/12
      \scaleDurations #'(2 . 3) {
         c'8
         d'8
         e'8
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}"


def test_measures_subsume_02( ):
   '''Subsume complete nonbinary tuplet.'''

   t = RigidMeasure((3, 16), [FixedDurationTuplet((3, 16), scale(5, (1, 16)))])
   measures_subsume(t)

   r'''
      \time 15/80
      \scaleDurations #'(4 . 5) {
         c'32.
         d'32.
         e'32.
         f'32.
         g'32.
      }
   '''
   
   assert check(t)
   assert t.format == "\t\\time 15/80\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'32.\n\t\td'32.\n\t\te'32.\n\t\tf'32.\n\t\tg'32.\n\t}"


def test_measures_subsume_03( ):
   '''Subsume 7:6 tuplet.'''

   t = RigidMeasure((6, 8), [FixedDurationTuplet((6, 8), scale(7))])
   measures_subsume(t)

   r'''
      \time 21/28
      \scaleDurations #'(4 . 7) {
         c'8.
         d'8.
         e'8.
         f'8.
         g'8.
         a'8.
         b'8.
      }
   '''

   assert check(t)
   assert t.format == "\t\\time 21/28\n\t\\scaleDurations #'(4 . 7) {\n\t\tc'8.\n\t\td'8.\n\t\te'8.\n\t\tf'8.\n\t\tg'8.\n\t\ta'8.\n\t\tb'8.\n\t}"


def test_measures_subsume_04( ):
   '''Subsume tuplet in nonassignable measure.'''

   t = RigidMeasure((5, 8), [FixedDurationTuplet((5, 8), scale(6))])
   measures_subsume(t)

   r'''
   \time 30/48
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

   assert check(t)
   assert t.format == "\t\\time 30/48\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8 ~\n\t\tc'32\n\t\td'8 ~\n\t\td'32\n\t\te'8 ~\n\t\te'32\n\t\tf'8 ~\n\t\tf'32\n\t\tg'8 ~\n\t\tg'32\n\t\ta'8 ~\n\t\ta'32\n\t}"


def test_measures_subsume_05( ):
   '''Subsume nested tuplet.'''

   inner = FixedDurationTuplet((2, 16), run(3, Rational(1, 16)))
   notes = run(2)
   outer = FixedDurationTuplet((2, 8), [inner] + notes)
   t = RigidMeasure((2, 8), [outer])
   diatonicize(t)

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

   assert check(t)
   assert t.format == "\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t}\n\t\tf'8\n\t\tg'8\n\t}"
