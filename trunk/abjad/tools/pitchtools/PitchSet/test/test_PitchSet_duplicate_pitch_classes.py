from abjad import *


def test_PitchSet_duplciate_pitch_classes_01( ):

   pset = pitchtools.PitchSet([0, 12, 13, 26])
  
   assert pset.duplicate_pitch_classes == pitchtools.PitchClassSet([0])


def test_PitchSet_duplciate_pitch_classes_02( ):

   pset = pitchtools.PitchSet([0, 13, 26])
  
   assert pset.duplicate_pitch_classes == pitchtools.PitchClassSet([ ])
