from abjad import *
from abjad.checks import MeasuresMisdurated
checker = MeasuresMisdurated( )



def test_measure_unmetered_01( ):
   t = Measure(None, Note(0, (1, 4)) * 4)
   assert repr(t) == "Measure([c'4, c'4, c'4, c'4])"
   assert str(t) == "|c'4, c'4, c'4, c'4|"
   assert t.format == "\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert t.meter == None
   assert len(t) == 4
   #assert t.duration == Rational(1)
   assert t.duration.preprolated == Rational(1)
   assert t.duration.prolated == Rational(1)
   assert checker.check(t)


def test_measure_unmetered_02( ):
   t = Measure(None, Note(0, (1, 4)) * 6)
   assert repr(t) == "Measure([c'4, c'4, c'4, c'4, c'4, c'4])"
   assert str(t) == "|c'4, c'4, c'4, c'4, c'4, c'4|"
   assert t.format == "\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert t.meter == None
   assert len(t) == 6
   #assert t.duration == Rational(6, 4)
   assert t.duration.preprolated == Rational(6, 4)
   assert t.duration.prolated == Rational(6, 4)
   assert checker.check(t)
