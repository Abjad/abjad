from abjad import *


def test_PitchSet_is_pitch_class_unique_01( ):

   pset = pitchtools.NamedPitchSet([0, 13, 26])
   assert pset.is_pitch_class_unique


def test_PitchSet_is_pitch_class_unique_02( ):

   pset = pitchtools.NamedPitchSet([0, 12, 13, 26])
   assert not pset.is_pitch_class_unique


def test_PitchSet_is_pitch_class_unique_03( ):
   '''Empty pitch-set and length-1 pitch-set boundary cases.'''

   assert pitchtools.NamedPitchSet([ ]).is_pitch_class_unique
   assert pitchtools.NamedPitchSet([13]).is_pitch_class_unique
