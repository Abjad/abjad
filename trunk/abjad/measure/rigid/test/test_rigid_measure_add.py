from abjad import *


def test_rigid_measure_add_01( ):
   '''Add outside-of-score rigid measures.'''
   
   t1 = RigidMeasure((1, 8), construct.scale(2, Rational(1, 16)))
   Beam(t1[:])
   t2 = RigidMeasure((2, 16), construct.scale(2, Rational(1, 16)))
   Slur(t2[:])

   r'''
   {
           \time 1/8
           c'16 [
           d'16 ]
   }
   '''

   r'''
   {
           \time 2/16
           c'16 (
           d'16 )
   }
   '''

   new = t1 + t2

   r'''
   {
           \time 2/8
           c'16 [
           d'16 ]
           c'16 (
           d'16 )
   }
   '''

   assert new is not t1 and new is not t2
   assert len(t1) == 0
   assert len(t2) == 0
   assert check.wf(new)
   assert new.format == "{\n\t\\time 2/8\n\tc'16 [\n\td'16 ]\n\tc'16 (\n\td'16 )\n}"

   
def test_rigid_measure_add_02( ):
   '''Add rigid measures in score.'''

   t1 = RigidMeasure((1, 8), construct.scale(2, Rational(1, 16)))
   Beam(t1[:])
   t2 = RigidMeasure((2, 16), construct.scale(2, Rational(1, 16)))
   Slur(t2[:])
   t = Staff([t1, t2])

   r'''
   \new Staff {
           {
                   \time 1/8
                   c'16 [
                   d'16 ]
           }
           {
                   \time 2/16
                   c'16 (
                   d'16 )
           }
   }
   '''
   
   new = t1 + t2

   r'''
   {
           \time 2/8
           c'16 [
           d'16 ]
           c'16 (
           d'16 )
   }
   '''

   assert new is not t1 and new is not t2
   assert len(t1) == 0
   assert len(t2) == 0
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 [\n\t\td'16 ]\n\t\tc'16 (\n\t\td'16 )\n\t}\n}"
