from abjad import *


def test_measuretools_move_prolation_of_full_measure_tuplet_to_meter_of_measure_01( ):
   '''Subsume complete binary tuplet.'''

   t = RigidMeasure((2, 8), [FixedDurationTuplet((2, 8), macros.scale(3))])
   measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

   r'''
   {
           \time 3/12
           \scaleDurations #'(2 . 3) {
                   c'8
                   d'8
                   e'8
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"


def test_measuretools_move_prolation_of_full_measure_tuplet_to_meter_of_measure_02( ):
   '''Subsume complete nonbinary tuplet.'''

   t = RigidMeasure((3, 16), [
      FixedDurationTuplet((3, 16), macros.scale(5, (1, 16)))])
   measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

   r'''
   {
           \time 15/80
           \scaleDurations #'(4 . 5) {
                   c'32.
                   d'32.
                   e'32.
                   f'32.
                   g'32.
           }
   }
   '''
   
   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 15/80\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'32.\n\t\td'32.\n\t\te'32.\n\t\tf'32.\n\t\tg'32.\n\t}\n}"


def test_measuretools_move_prolation_of_full_measure_tuplet_to_meter_of_measure_03( ):
   '''Subsume 7:6 tuplet.'''

   t = RigidMeasure((6, 8), [
      FixedDurationTuplet((6, 8), macros.scale(7))])
   measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

   r'''
   {
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
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 21/28\n\t\\scaleDurations #'(4 . 7) {\n\t\tc'8.\n\t\td'8.\n\t\te'8.\n\t\tf'8.\n\t\tg'8.\n\t\ta'8.\n\t\tb'8.\n\t}\n}"


def test_measuretools_move_prolation_of_full_measure_tuplet_to_meter_of_measure_04( ):
   '''Subsume tuplet in nonassignable measure.'''

   t = RigidMeasure((5, 8), [
      FixedDurationTuplet((5, 8), macros.scale(6))])
   measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

   r'''
   {
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
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 15/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8 ~\n\t\tc'32\n\t\td'8 ~\n\t\td'32\n\t\te'8 ~\n\t\te'32\n\t\tf'8 ~\n\t\tf'32\n\t\tg'8 ~\n\t\tg'32\n\t\ta'8 ~\n\t\ta'32\n\t}\n}"


def test_measuretools_move_prolation_of_full_measure_tuplet_to_meter_of_measure_05( ):
   '''Subsume nested tuplet.'''

   inner = FixedDurationTuplet((2, 16), leaftools.make_repeated_notes(3, Rational(1, 16)))
   notes = leaftools.make_repeated_notes(2)
   outer = FixedDurationTuplet((2, 8), [inner] + notes)
   t = RigidMeasure((2, 8), [outer])
   pitchtools.diatonicize(t)

   r'''
   {
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
   }
   '''

   measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

   r'''
   {
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
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t}\n\t\tf'8\n\t\tg'8\n\t}\n}"


def test_measuretools_move_prolation_of_full_measure_tuplet_to_meter_of_measure_06( ):
   '''Submsume 6:5. Meter should go from 5/16 to 15/48.'''

   tuplet = FixedDurationTuplet((5, 16), macros.scale(3))
   t = RigidMeasure((5, 16), [tuplet])

   r'''
   {
           \time 5/16
           \fraction \times 5/6 {
                   c'8
                   d'8
                   e'8
           }
   }
   '''

   measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure(t)

   r'''
   {
           \time 15/48
           \scaleDurations #'(2 . 3) {
                   c'8 ~
                   c'32
                   d'8 ~
                   d'32
                   e'8 ~
                   e'32
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "{\n\t\\time 15/48\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8 ~\n\t\tc'32\n\t\td'8 ~\n\t\td'32\n\t\te'8 ~\n\t\te'32\n\t}\n}"
