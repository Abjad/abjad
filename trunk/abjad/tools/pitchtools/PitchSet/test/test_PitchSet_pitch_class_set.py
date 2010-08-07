from abjad import *


def test_PitchSet_pitch_class_set_01( ):

   pset = pitchtools.PitchSet([0, 13, 26])
   pcset = pitchtools.NumericPitchClassSet([0, 1, 2])
   
   assert pset.pitch_class_set == pitchtools.NumericPitchClassSet([0, 1, 2])
