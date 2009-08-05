from abjad import *


def test_dynamic_measure_duration_interface_01( ):
   '''Notes as contents.'''

   t = DynamicMeasure(construct.scale(4))
   t.denominator = 8

   r'''
   {
           \time 4/8
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.duration.contents == Rational(4, 8)
   assert t.duration.preprolated == Rational(4, 8)
   assert t.duration.prolated == Rational(4, 8)
   assert t.duration.prolation == 1

   assert t.format == "{\n\t\\time 4/8\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_dynamic_measure_duration_interface_02( ):
   '''Binary tuplet as contents.'''

   t = DynamicMeasure([FixedDurationTuplet((2, 8), construct.scale(3))])
   t.denominator = 8

   r'''
   {
           \time 2/8
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
   }
   '''

   assert t.duration.contents == Rational(2, 8)
   assert t.duration.preprolated == Rational(2, 8)
   assert t.duration.prolated == Rational(2, 8)
   assert t.duration.prolation == 1

   assert t.format == "{\n\t\\time 2/8\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"


def test_dynamic_measure_duration_interface_03( ):
   '''Nonbinary tuplet as contents.'''

   t = DynamicMeasure([FixedMultiplierTuplet((2, 3), construct.scale(4))])
   t.denominator = 12

   r'''
   {
           \time 4/12
           \times 2/3 {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   }
   '''

   assert t.duration.contents == Rational(4, 12)
   assert t.duration.preprolated == Rational(4, 12)
   assert t.duration.prolated == Rational(4, 12)
   assert t.duration.prolation == 1

   assert t.format == "{\n\t\\time 4/12\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"
