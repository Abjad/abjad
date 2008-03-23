from abjad import *
from abjad.wf import check_measures


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


def test_measure_duration_mismatch_05( ):
   t = Measure((5, 9), Note(0, (1, 8)) * 4)
   assert not check_measures(t, ret = True)


def test_measure_duration_mismatch_06( ):
   t = Measure((5, 9), Note(0, (1, 16)) * 5)
   assert not check_measures(t, ret = True)


def test_measure_duration_mismatch_07( ):
   t = Measure((5, 9), [ ])
   assert not check_measures(t, ret = True)


def test_measure_duration_mismatch_08( ):
   t = Measure((4, 9), [ ])
   assert not check_measures(t, ret = True)
