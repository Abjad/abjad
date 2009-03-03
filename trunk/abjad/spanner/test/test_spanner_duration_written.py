from abjad import *


def test_spanner_duration_written_01( ):
   t = Voice([RigidMeasure((2, 12), scale(2)), RigidMeasure((2, 8), scale(2))])
   beam = Beam(t.leaves)
   crescendo = Crescendo(t[0][:])
   decrescendo = Decrescendo(t[1][:])

   assert beam.written == Rational(4, 8)
   assert crescendo.written == Rational(2, 8)
   assert decrescendo.written == Rational(2, 8)
   
