from abjad import *


def test_PitchClassSet_interval_class_set_01( ):

   pcset = pitchtools.PitchClassSet([0, 6, 10, 4, 9, 2])

   icset = pitchtools.IntervalClassSet([1, 2, 3, 4, 5, 6])
   assert pcset.interval_class_set == icset
