from abjad import *


def test_NumberedChromaticPitchClass_semitones_01( ):

   assert pitchtools.NumberedChromaticPitchClass(0).semitones == 0
   assert pitchtools.NumberedChromaticPitchClass(0.5).semitones == 0.5
   assert pitchtools.NumberedChromaticPitchClass(1).semitones == 1
   assert pitchtools.NumberedChromaticPitchClass(1.5).semitones == 1.5


def test_NumberedChromaticPitchClass_semitones_02( ):

   assert pitchtools.NumberedChromaticPitchClass(12).semitones == 0
   assert pitchtools.NumberedChromaticPitchClass(12.5).semitones == 0.5
   assert pitchtools.NumberedChromaticPitchClass(13).semitones == 1
   assert pitchtools.NumberedChromaticPitchClass(13.5).semitones == 1.5
