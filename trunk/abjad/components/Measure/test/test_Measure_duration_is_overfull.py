from abjad import *


def test_Measure_duration_is_overfull_01( ):

   t = Measure((3, 8), notetools.make_repeated_notes(3))
   assert not t.duration.is_overfull

   contexttools.TimeSignatureMark(2, 8)(t)
   assert t.duration.is_overfull

   contexttools.TimeSignatureMark(3, 8)(t)
   assert not t.duration.is_overfull
