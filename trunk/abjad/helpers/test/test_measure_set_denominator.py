from abjad import *


def test_measure_set_denominator_01( ):

   t = RigidMeasure((3, 8), scale(3))
   measure_set_denominator(t, 16)

   r'''  \time 6/16
      c'8
      d'8
      e'8'''

   assert check(t)
   assert t.format == "\t\\time 6/16\n\tc'8\n\td'8\n\te'8"

   measure_set_denominator(t, 8)

   r'''  \time 3/8
      c'8
      d'8
      e'8'''

   assert check(t)
   assert t.format == "\t\\time 3/8\n\tc'8\n\td'8\n\te'8"
