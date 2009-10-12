from abjad import *


def test_pitchtools_PitchClass_transpose_01( ):
   
   pc = pitchtools.PitchClass(1)
   assert pc.transpose(0) == pitchtools.PitchClass(1)
   assert pc.transpose(1) == pitchtools.PitchClass(2)
   assert pc.transpose(-1) == pitchtools.PitchClass(0)
   assert pc.transpose(99) == pitchtools.PitchClass(4)
   assert pc.transpose(-99) == pitchtools.PitchClass(10)
