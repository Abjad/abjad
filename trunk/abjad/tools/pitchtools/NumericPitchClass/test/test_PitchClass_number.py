from abjad import *


def test_PitchClass_number_01( ):

   assert pitchtools.PitchClass(0).number == 0
   assert pitchtools.PitchClass(0.5).number == 0.5
   assert pitchtools.PitchClass(1).number == 1
   assert pitchtools.PitchClass(1.5).number == 1.5


def test_PitchClass_number_02( ):

   assert pitchtools.PitchClass(12).number == 0
   assert pitchtools.PitchClass(12.5).number == 0.5
   assert pitchtools.PitchClass(13).number == 1
   assert pitchtools.PitchClass(13.5).number == 1.5
