from abjad import *
import py.test


def test_containertools_multiplier_set_01( ):
   '''Set multiplier on fixed-duration tuplet 
      by adjusting target duration.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))
   assert t.duration.target == Rational(2, 8)
   assert t.duration.multiplier == Rational(2, 3)

   containertools.multiplier_set(t, Rational(5, 8))
   assert t.duration.target == Rational(15, 64)
   assert t.duration.multiplier == Rational(5, 8)


def test_containertools_multiplier_set_02( ):
   '''Set multiplier on rigid measure by adjusting meter.'''

   t = RigidMeasure((3, 8), construct.scale(3))
   assert t.meter.effective.duration == Rational(3, 8)

   containertools.multiplier_set(t, Rational(2, 3))
   assert t.meter.effective.duration == Rational(2, 8)
   assert py.test.raises(OverfullMeasureError, 't.format')
