from abjad import *
import py.test


def test_containertools_set_container_multiplier_01( ):
   '''Set multiplier on fixed-duration tuplet 
      by adjusting target duration.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   assert t.duration.target == Rational(2, 8)
   assert t.duration.multiplier == Rational(2, 3)

   containertools.set_container_multiplier(t, Rational(5, 8))
   assert t.duration.target == Rational(15, 64)
   assert t.duration.multiplier == Rational(5, 8)


def test_containertools_set_container_multiplier_02( ):
   '''Set multiplier on rigid measure by adjusting meter.'''

   t = RigidMeasure((3, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   assert t.meter.effective.duration == Rational(3, 8)

   containertools.set_container_multiplier(t, Rational(2, 3))
   assert t.meter.effective.duration == Rational(2, 8)
   assert py.test.raises(OverfullMeasureError, 't.format')
