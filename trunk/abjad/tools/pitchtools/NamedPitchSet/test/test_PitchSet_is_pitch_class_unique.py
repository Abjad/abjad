from abjad import *


def test_PitchSet_is_pitch_class_unique_01( ):

   pset = pitchtools.PitchSet([0, 13, 26])
   assert pset.is_pitch_class_unique


def test_PitchSet_is_pitch_class_unique_02( ):

   pset = pitchtools.PitchSet([0, 12, 13, 26])
   assert not pset.is_pitch_class_unique


def test_PitchSet_is_pitch_class_unique_03( ):
   '''Empty pitch-set and length-1 pitch-set boundary cases.'''

   assert pitchtools.PitchSet([ ]).is_pitch_class_unique
   assert pitchtools.PitchSet([13]).is_pitch_class_unique
