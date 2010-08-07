from abjad import *


def test_NumericPitchClass_number_01( ):

   assert pitchtools.NumericPitchClass(0).number == 0
   assert pitchtools.NumericPitchClass(0.5).number == 0.5
   assert pitchtools.NumericPitchClass(1).number == 1
   assert pitchtools.NumericPitchClass(1.5).number == 1.5


def test_NumericPitchClass_number_02( ):

   assert pitchtools.NumericPitchClass(12).number == 0
   assert pitchtools.NumericPitchClass(12.5).number == 0.5
   assert pitchtools.NumericPitchClass(13).number == 1
   assert pitchtools.NumericPitchClass(13.5).number == 1.5
