from abjad import *


def test_PitchClass_transpose_01( ):
   
   pc = pitchtools.NumericPitchClass(1)
   assert pc.transpose(0) == pitchtools.NumericPitchClass(1)
   assert pc.transpose(1) == pitchtools.NumericPitchClass(2)
   assert pc.transpose(-1) == pitchtools.NumericPitchClass(0)
   assert pc.transpose(99) == pitchtools.NumericPitchClass(4)
   assert pc.transpose(-99) == pitchtools.NumericPitchClass(10)
