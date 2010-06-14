from abjad import *


def test_rigid_measure_duration_is_overfull_01( ):

   t = RigidMeasure((3, 8), leaftools.make_repeated_notes(3))
   assert not t.duration.is_overfull

   t.meter.forced = Meter(2, 8)
   assert t.duration.is_overfull

   t.meter.forced = Meter(3, 8)
   assert not t.duration.is_overfull
