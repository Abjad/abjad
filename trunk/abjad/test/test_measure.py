from abjad import *
from abjad.wf import check_measures_durations


### TEST TYPICAL MEASURE ###

def test_typical_measure_01( ):
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   assert repr(t) == "Measure(4/4, [c'4, c'4, c'4, c'4])"
   assert str(t) == "|4/4, c'4, c'4, c'4, c'4|"
   assert t.format == "\t\\time 4/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert len(t) == 4
   assert t.duration == Rational(1)
   assert t.duration.prolated == Rational(1)
   assert check_measures_durations(t, ret = True)


### TEST UNMETERED MEASURE ###

def test_unmetered_measure_01( ):
   t = Measure(None, Note(0, (1, 4)) * 4)
   assert repr(t) == "Measure([c'4, c'4, c'4, c'4])"
   assert str(t) == "|c'4, c'4, c'4, c'4|"
   assert t.format == "\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert t.meter == None
   assert len(t) == 4
   assert t.duration == Rational(1)
   assert t.duration.prolated == Rational(1)
   assert check_measures_durations(t, ret = True)
