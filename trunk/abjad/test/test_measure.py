from abjad import *
from abjad.wf import check_measures


### TEST TYPICAL MEASURE ###

def test_typical_measure_01( ):
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   assert repr(t) == "Measure(4/4, [c'4, c'4, c'4, c'4])"
   assert str(t) == "|4/4, c'4, c'4, c'4, c'4|"
   assert t.format == "\t\\time 4/4\n\tc'4\n\tc'4\n\tc'4\n\tc'4"
   #assert t.meter == Meter(4, 4)
   assert len(t) == 4
   assert t.duration == Rational(1)
   assert t.duration.absolute == Rational(1)
   assert check_measures(t, ret = True)


### TEST UNMETERED MEASURE ###

def test_unmetered_measure_01( ):
   t = Measure(None, Note(0, (1, 4)) * 4)
   assert repr(t) == "Measure([c'4, c'4, c'4, c'4])"
   assert str(t) == "|c'4, c'4, c'4, c'4|"
   assert t.format == "\tc'4\n\tc'4\n\tc'4\n\tc'4"
   assert t.meter == None
   assert len(t) == 4
   assert t.duration == Rational(1)
   assert t.duration.absolute == Rational(1)
   assert check_measures(t, ret = True)


### TEST EMPTY MEASURE ###

def test_empty_measure_01( ):
   t = Measure(None, [ ])
   assert repr(t) == 'Measure( )'
   assert str(t) == '| |'
   assert t.format == ''
   assert t.meter == None
   assert len(t) == 0
   assert t.duration == Rational(0)
   assert t.duration.absolute == Rational(0)
   assert check_measures(t, ret = True)

def test_empty_measure_02( ):
   t = Measure((4, 4), [ ])
   assert repr(t) == 'Measure(4/4)'
   assert str(t) == '|4/4|'
   assert t.format == '\t\\time 4/4'
   #assert t.meter == Meter(4, 4)
   assert len(t) == 0
   assert t.duration == Rational(0)
   assert t.duration.absolute == Rational(0)
   assert not check_measures(t, ret = True)


### TEST MEASURE DURATION MISMATCH ###

def test_measure_duration_mismatch_01( ):
   t = Measure((5, 8), Note(0, (1, 8)) * 4)
   assert not check_measures(t, ret = True)

def test_measure_duration_mismatch_02( ):
   t = Measure((5, 8), Note(0, (1, 16)) * 5)
   assert not check_measures(t, ret = True)

def test_measure_duration_mismatch_03( ):
   t = Measure((5, 8), [ ])
   assert not check_measures(t, ret = True)

def test_measure_duration_mismatch_04( ):
   t = Measure((4, 8), [ ])
   assert not check_measures(t, ret = True)


### TEST GRAFT MEASURE TO CONTAINER ###

def test_graft_measure_to_container_01( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   t[0 : 4] = [Measure((4, 8), t[0 : 4])]
   leaves_after = t.leaves
   assert len(t) == 5
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures(t, ret = True)

def test_graft_measure_to_container_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   t[0 : 4] = [Measure((4, 8), t[0 : 4])]
   leaves_after = t.leaves
   assert len(t) == 5
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures(t, ret = True)

def test_graft_measure_to_container_03( ):
   t = Staff([Note(n, (1, 1)) for n in range(4)])
   leaves_before = t.leaves
   t[0] = Measure((1, 1), t[0 : 1])
   leaves_after = t.leaves
   assert len(t) == 4
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures(t, ret = True)

def test_graft_measure_to_container_03( ):
   t = Staff([Note(n, (1, 1)) for n in range(4)])
   leaves_before = t.leaves
   t[-1] = Measure((1, 1), t[-1 : ])
   leaves_after = t.leaves
   assert len(t) == 4
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == len(t) - 1:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures(t, ret = True)
