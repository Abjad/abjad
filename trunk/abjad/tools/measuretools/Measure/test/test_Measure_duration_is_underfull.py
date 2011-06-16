from abjad import *


def test_Measure_duration_is_underfull_01( ):

   t = Measure((3, 8), notetools.make_repeated_notes(3))
   assert not t.duration.is_underfull

   contexttools.TimeSignatureMark(4, 8)(t)
   assert t.duration.is_underfull

   contexttools.TimeSignatureMark(3, 8)(t)
   assert not t.duration.is_underfull
