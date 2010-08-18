from abjad import *


def test_RigidMeasure_duration_is_overfull_01( ):

   t = Measure((3, 8), notetools.make_repeated_notes(3))
   assert not t.duration.is_overfull

   t.meter.forced = metertools.Meter(2, 8)
   assert t.duration.is_overfull

   t.meter.forced = metertools.Meter(3, 8)
   assert not t.duration.is_overfull
