from abjad import *
import py.test


def test_rigid_measure_duration_interface_01( ):
   '''Binary meter, properly filled.'''

   t = RigidMeasure((3, 8), construct.scale(3))

   r'''
   {
           \time 3/8
           c'8
           d'8
           e'8
   }
   '''

   assert t.duration.contents == Rational(3, 8)
   assert t.duration.preprolated == Rational(3, 8)
   assert t.duration.prolated == Rational(3, 8)
   assert t.duration.prolation == 1

   assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"


def test_rigid_measure_duration_interface_02( ):
   '''Nonbinary meter, properly filled.'''

   t = RigidMeasure((3, 10), construct.scale(3))

   r'''
   {
           \time 3/10
           \scaleDurations #'(4 . 5) {
                   c'8
                   d'8
                   e'8
           }
   }
   '''

   assert t.duration.contents == Rational(3, 8)
   assert t.duration.preprolated == Rational(3, 10)
   assert t.duration.prolated == Rational(3, 10)
   assert t.duration.prolation == 1

   assert t.format == "{\n\t\\time 3/10\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n}"


def test_rigid_measure_duration_interface_03( ):
   '''Binary meter, improperly filled.'''

   t = RigidMeasure((3, 8), construct.scale(4))

   assert py.test.raises(OverfullMeasureError, 't.format')
   
   assert t.duration.contents == Rational(4, 8)
   assert t.duration.preprolated == Rational(4, 8)
   assert t.duration.prolated == Rational(4, 8)
   assert t.duration.prolation == 1


def test_rigid_measure_duration_interface_04( ):
   '''Nonbinary meter, improperly filled.'''

   t = RigidMeasure((3, 10), construct.scale(4))

   assert py.test.raises(OverfullMeasureError, 't.format')

   assert t.duration.contents == Rational(4, 8)
   assert t.duration.preprolated == Rational(4, 10)
   assert t.duration.prolated == Rational(4, 10)
   assert t.duration.prolation == 1
