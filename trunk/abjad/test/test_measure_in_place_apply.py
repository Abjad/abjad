from abjad import *
from abjad.wf import check_measures_durations



### NEW IN-PLACE APPLICATION SYNTAX ###


def test_measure_in_place_apply_01( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   Measure((4, 8), t[0 : 4])
   leaves_after = t.leaves
   assert len(t) == 5
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures_durations(t, ret = True)


def test_measure_in_place_apply_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   leaves_before = t.leaves
   Measure((4, 8), t[0 : 4])
   leaves_after = t.leaves
   assert len(t) == 5
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures_durations(t, ret = True)


def test_measure_in_place_apply_03( ):
   t = Staff([Note(n, (1, 1)) for n in range(4)])
   leaves_before = t.leaves
   Measure((1, 1), t[0 : 1])
   leaves_after = t.leaves
   assert len(t) == 4
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == 0:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures_durations(t, ret = True)


def test_measure_in_place_apply_04( ):
   t = Staff([Note(n, (1, 1)) for n in range(4)])
   leaves_before = t.leaves
   Measure((1, 1), t[-1 : ])
   leaves_after = t.leaves
   assert len(t) == 4
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      if i == len(t) - 1:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check_measures_durations(t, ret = True)
