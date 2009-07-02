from abjad import *


def test_measuretools_denominator_set_01( ):

   t = RigidMeasure((3, 8), construct.scale(3))
   measuretools.denominator_set(t, 16)

   r'''
   {
           \time 6/16
           c'8
           d'8
           e'8
   }
   '''

   assert check.wf(t)
   assert t.format == "{\n\t\\time 6/16\n\tc'8\n\td'8\n\te'8\n}"

   measuretools.denominator_set(t, 8)

   r'''
   {
           \time 3/8
           c'8
           d'8
           e'8
   }
   '''

   assert check.wf(t)
   assert t.format == "{\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n}"
