from abjad import *


def test_RigidMeasure_duration_is_underfull_01( ):

   t = RigidMeasure((3, 8), leaftools.make_repeated_notes(3))
   assert not t.duration.is_underfull

   t.meter.forced = Meter(4, 8)
   assert t.duration.is_underfull

   t.meter.forced = Meter(3, 8)
   assert not t.duration.is_underfull
