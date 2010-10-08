from abjad import *


def test_NumberedChromaticPitchClass_number_01( ):

   assert pitchtools.NumberedChromaticPitchClass(0).number == 0
   assert pitchtools.NumberedChromaticPitchClass(0.5).number == 0.5
   assert pitchtools.NumberedChromaticPitchClass(1).number == 1
   assert pitchtools.NumberedChromaticPitchClass(1.5).number == 1.5


def test_NumberedChromaticPitchClass_number_02( ):

   assert pitchtools.NumberedChromaticPitchClass(12).number == 0
   assert pitchtools.NumberedChromaticPitchClass(12.5).number == 0.5
   assert pitchtools.NumberedChromaticPitchClass(13).number == 1
   assert pitchtools.NumberedChromaticPitchClass(13.5).number == 1.5
