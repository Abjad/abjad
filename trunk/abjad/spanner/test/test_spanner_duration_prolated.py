from abjad import *


def test_spanner_duration_prolated_01( ):
   t = Voice([RigidMeasure((2, 12), scale(2)), RigidMeasure((2, 8), scale(2))])
   beam = Beam(t.leaves)
   crescendo = Crescendo(t[0][:])
   decrescendo = Decrescendo(t[1][:])

   assert beam.duration.prolated == Rational(5, 12)
   assert crescendo.duration.prolated == Rational(2, 12)
   assert decrescendo.duration.prolated == Rational(2, 8)
