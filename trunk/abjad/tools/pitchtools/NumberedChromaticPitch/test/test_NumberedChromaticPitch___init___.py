from abjad import *


def test_NumberedChromaticPitch___init____01( ):
   '''Init with number.'''

   assert pitchtools.NumberedChromaticPitch(0).number == 0
   assert pitchtools.NumberedChromaticPitch(0.5).number == 0.5
   assert pitchtools.NumberedChromaticPitch(12).number == 12
   assert pitchtools.NumberedChromaticPitch(12.5).number == 12.5
   assert pitchtools.NumberedChromaticPitch(-12).number == -12
   assert pitchtools.NumberedChromaticPitch(-12.5).number == -12.5


def test_NumberedChromaticPitch___init____02( ):
   '''Init with other numeric pitch instance.'''

   assert pitchtools.NumberedChromaticPitch(pitchtools.NumberedChromaticPitch(12)).number == 12
