from abjad import *


def test_RigidMeasure_duration_is_underfull_01( ):

   t = Measure((3, 8), notetools.make_repeated_notes(3))
   assert not t.duration.is_underfull

   #t.meter.forced = metertools.Meter(4, 8)
   marktools.TimeSignatureMark(4, 8)(Staff, t)
   assert t.duration.is_underfull

   #t.meter.forced = metertools.Meter(3, 8)
   marktools.TimeSignatureMark(3, 8)(Staff, t)
   assert not t.duration.is_underfull
